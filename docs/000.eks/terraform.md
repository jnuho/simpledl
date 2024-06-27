
https://antonputra.com/terraform/how-to-create-eks-cluster-using-terraform/#create-public-load-balancer-on-eks

https://honglab.tistory.com/119


# Install terraform

- Download terraform.exe

시스템변수 > Path에 추가 C:\terraform


# Apply Terraform

```sh
trraform init
terraform plan
terraform apply
terraform destroy
```

# AWS cli configuration

```sh
aws configure
aws configure --profile terraform
```

# SG for EKS

open for EC2 bastion 

All traffic 172.16.0.0/16


# 8-iam-oidc.tf

- Create IAM OIDC provider EKS using Terraform

```
To manage permissions for your applications that you deploy in Kubernetes. You can either attach policies to Kubernetes nodes directly. In that case, every pod will get the same access to AWS resources. Or you can create OpenID connect provider, which will allow granting IAM permissions based on the service account used by the pod. File name is terraform/8-iam-oidc.tf.
```

# 9-iam-test.tf

I highly recommend testing the provider first before deploying the autoscaller. It can save you a lot of time. File name is terraform/9-iam-test.tf.

```tf
# Create iam role with vpc_cni_trust_policy and output its arn
#   validate OpenID connect provider?

# Equivalent to vpc-cni-trust-policy.json

data "aws_iam_policy_document" "test_oidc_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:default:aws-test"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "test_oidc" {
  assume_role_policy = data.aws_iam_policy_document.test_oidc_assume_role_policy.json
  name               = "test-oidc"
}


# Attach AWS S3 policy to 'test-oidc' IAM Role
#   annotate a Service Account with this IAM Role
#   connect this Service Account with a test Pod.
resource "aws_iam_policy" "test-policy" {
  name = "test-policy"

  policy = jsonencode({
    Statement = [{
      Action = [
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation"
      ]
      Effect   = "Allow"
      Resource = "arn:aws:s3:::*"
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "test_attach" {
  role       = aws_iam_role.test_oidc.name
  policy_arn = aws_iam_policy.test-policy.arn
}

output "test_policy_arn" {
  value = aws_iam_role.test_oidc.arn
}
```

# 10-update-cluser.sh

```sh
aws eks --region ap-northeast-2 update-kubeconfig --name testcluster-001
```

- Next is to create a pod to test IAM roles for service accounts.
  - Create service account
  - Use it in your Pod spec (can be deployment, replicaset, or jobs)
  - First, we are going to omit annotations to bind the service account with the role
  - then bind ServiceAccount with 'test_oidc' role.


# 11-aws-test-sa.yaml

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-test
  namespace: default
---

# use above serviceaccount in a Pod
apiVersion: v1
kind: Pod
metadata:
  name: aws-cli
  namespace: default
spec:
  serviceAccountName: aws-test
  containers:
  - name: aws-cli
    image: amazon/aws-cli
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
  tolerations:
  - operator: Exists
    effect: NoSchedule
```


```sh
kubectl apply -f 11-aws-test-sa.yaml

# check if it can list s3 list
kubectl exec aws-cli -- aws s3api list-buckets
```

- [aws_iam_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document)

```
Generates an IAM policy document in JSON format for use with resources that expect policy documents such as aws_iam_policy.
```

- Let's add missing annotation to the service account and redeploy the pod.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-test
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::094833749257:role/test-oidc
---

```


```sh
kubectl delete -f 11-aws-test-sa.yaml
kubectl apply -f 11-aws-test-sa.yaml


kubectl exec aws-cli -- aws s3api list-buckets
```


# Create public load balancer on EKS¶

Next, let's deploy the sample application and expose it using public and private load balancers.
The first is a deployment object with a base nginx image. File name is k8s/deployment.yaml.

# 12-deployment.yaml:

```
metadata.labels 필드는 Deployment자체의 label
spec.selector.matchLabels 필드는 Pod의 label
spec.selector.matchLabels == spec.template.metadata.labels
```

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx

  # Labels for deployment
  labels:
    app: nginx
spec:
  replicas: 1

  # Labels for pod
  selector:
    matchLabels:
      app: nginx
  template:
    # metadata 
    # Same label info for Pod
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - name: web
          containerPort: 80
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 256Mi
            cpu: 250m
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: role
                operator: In
                values:
                - general
      # tolerations:
      # - key: team
      #   operator: Equal
      #   value: devops
      #   effect: NoSchedule

```

```sh
k get deploy -l app=nginx -n default
```


# 13-public-lb.yaml


```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: public-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: web
```



# 14-private-lb.yaml

- Create private load balancer on EKS


```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: private-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-internal: 0.0.0.0/0
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: web
```

# 15-iam-autoscaler.tf

- Deploy EKS cluster autoscaler

```yaml
data "aws_iam_policy_document" "eks_cluster_autoscaler_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:cluster-autoscaler"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "eks_cluster_autoscaler" {
  assume_role_policy = data.aws_iam_policy_document.eks_cluster_autoscaler_assume_role_policy.json
  name               = "eks-cluster-autoscaler"
}

resource "aws_iam_policy" "eks_cluster_autoscaler" {
  name = "eks-cluster-autoscaler"

  policy = jsonencode({
    Statement = [{
      Action = [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeTags",
                "autoscaling:SetDesiredCapacity",
                "autoscaling:TerminateInstanceInAutoScalingGroup",
                "ec2:DescribeLaunchTemplateVersions"
            ]
      Effect   = "Allow"
      Resource = "*"
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_autoscaler_attach" {
  role       = aws_iam_role.eks_cluster_autoscaler.name
  policy_arn = aws_iam_policy.eks_cluster_autoscaler.arn
}

output "eks_cluster_autoscaler_arn" {
  value = aws_iam_role.eks_cluster_autoscaler.arn
}
```




#  16-cluster-autoscaler.yaml

- https://github.com/antonputra/tutorials/blob/main/lessons/102/k8s/cluster-autoscaler.yaml

```yaml
```


```sh
kubectl apply -f 15-cluster-autoscaler.yaml

kubectl get pods -n kube-system
kubectl logs -l app=cluster-autoscaler -n kube-system -f

watch -n 1 -t kubectl get pods
watch -n 1 -t kubectl get nodes
```

# 10-loadbalancer-controller.tf

https://wrynn.tistory.com/66

An API object that manages external access to the services in a cluster, typically HTTP.

- load balancer controller
  - https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html

```sh
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json

# Create an IAM role.
# Create a Kubernetes service account named aws-load-balancer-controller in the kube-system namespace
# for the AWS Load Balancer Controller
# and annotate the Kubernetes service account with the name of the IAM role.
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json


oidc_id=$(aws eks describe-cluster --name testcluster-001 --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)

aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4

cat >load-balancer-role-trust-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com",
                    "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
                }
            }
        }
    ]
}
EOF


aws iam create-role \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --assume-role-policy-document file://"load-balancer-role-trust-policy.json"
```



