

https://github.com/aws/aws-k8s-tester


- [Setting Up](#setting-up)
- [Getting started with Amazon EKS](#Getting-started-with-Amazon-EKS)
  - [eksctl](#eksctl)
  - [AWS Management Console and AWS CLI](#AWS-Management-Console-and-AWS-CLI)
- [Add-ons](#add-ons)

# Setting Up

1. aws-cli
  - create IAM user and generate access key (download .csv)
  - (optional) get security token

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html


```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure Access key, Secret key, region, and etc
aws configure
aws configure --profile [PROFILE_NAME]

# To verify the user identity
aws sts get-caller-identity
```

2. eksctl

https://eksctl.io/installation/

- install-eksctl.sh

```sh
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin
```

3. kubectl

- https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

```sh
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
kubectl version --client
```

- TODO kubectl 클러스터와 통신 구성
  - After cluster creation

```sh
aws sts get-caller-identity

aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster

# Edit SG for EKS inbound rules:
# All traffic 172.16.0.0/16
```


# Getting started with Amazon EKS

- Create EKS cluster using one of the followings
  - eksctl command
  - AWS Management Console and AWS CLI

## eksctl

- eksctl uses cloudformation

```sh
# The cluster configuration is created in ~/.kube/config
eksctl create cluster --name my-cluster --region ap-northeast-2
eksctl create cluster --name my-cluster --region ap-northeast-2 --profile kams

eksctl delete cluster --name my-cluster --region ap-northeast-2
```

- kubectl 클러스터 통신 설정
  - Configures kubectl so that you can connect to an Amazon EKS cluster.
  - Configuration file is created in `~/.kube/config`

```sh
aws sts get-caller-identity
aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster
aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster --profile kams

kubectl get no -o wide
kubectl get pods -A -o wide
```

## AWS Management Console and AWS CLI

https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html
https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html

1. Create an Amazon VPC
  - https://docs.aws.amazon.com/eks/latest/userguide/creating-a-vpc.html
  - 1. public and private subnets that meets Amazon EKS requirements
    - public route table has a route to an internet gateway
    - private route table does not have a route to an internet gateway
      - instead it uses NAT gateway;
      - Pods in private subnet can communicate to the internet through a NAT gateway using IPv4 addresses
  - 2. public only subnets
  - 3. private only subnets

```sh
aws cloudformation create-stack \
  --region ap-northeast-2 \
  --stack-name my-eks-vpc-stack \
  --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml

# 172.16.0.0/16 으로 수정하여 stack 생성
aws cloudformation create-stack \
  --region ap-northeast-2 \
  --stack-name my-eks-vpc-stack \
  --template-body file://amazon-eks-vpc-sample.yaml
```

2. EKS cluster IAM Role creation

https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html

```sh
cat > eks-cluster-role-trust-policy.json <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name myAmazonEKSClusterRole \
  --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"

# Attach the required Amazon EKS managed IAM policy to the role
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy \
  --role-name myAmazonEKSClusterRole

aws iam list-roles | grep RoleName
```

3. EKS cluster creation

- Create EKS cluster using AWS management console
- Go to EKS > Add cluster > Create
  - Enter name
  - Choose Cluster Service Role
  - Specify networking: VPC
  - Add-ons (Check 5. Add-ons below)
    - https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html

- Check EKS addon such as VPC-cni, CoreDNS Version, and kube-proxy with below URL
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-kube-proxy.html

4. EKS kubeconfig setting

```sh
aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster
kubectl get svc
```


5. Add-ons

- EKS cluster oidc registration

```
To use some Amazon EKS add-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management (IAM) permissions, create an IAM OpenID Connect (OIDC) provider for your cluster. You only need to create an IAM OIDC provider for your cluster once. To learn more about Amazon EKS add-ons, see Amazon EKS add-ons. To learn more about assigning specific IAM permissions to your workloads, see IAM roles for service accounts.
```

- https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html

- Check EKS addon such as VPC-cni, CoreDNS Version, and kube-proxy with below URL
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html
  - https://docs.aws.amazon.com/eks/latest/userguide/managing-kube-proxy.html

```sh
# Determine available list of add-ons for specified EKS version
#   vpc-cni, coredns, kube-proxy are default add-ons
aws eks describe-addon-versions --kubernetes-version 1.28 \
    --query 'addons[].{MarketplaceProductUrl: marketplaceInformation.productUrl, Name: addonName, Owner: owner Publisher: publisher, Type: type}' --output table

# You can see which versions are available for each add-on
#   vpc-cni
aws eks describe-addon-versions --kubernetes-version 1.28 --addon-name vpc-cni \
    --query 'addons[].addonVersions[].{Version: addonVersion, Defaultversion: compatibilities[0].defaultVersion}' --output table
  ------------------------------------------
  |          DescribeAddonVersions         |
  +-----------------+----------------------+
  | Defaultversion  |       Version        |
  +-----------------+----------------------+
  |  False          |  v1.16.0-eksbuild.1  |
  |  False          |  v1.15.5-eksbuild.1  |
  |  True           |  v1.14.1-eksbuild.1  |
  ...
  +-----------------+----------------------+

#   coredns
aws eks describe-addon-versions --kubernetes-version 1.28 --addon-name coredns \
    --query 'addons[].addonVersions[].{Version: addonVersion, Defaultversion: compatibilities[0].defaultVersion}' --output table

  ------------------------------------------
  |          DescribeAddonVersions         |
  +-----------------+----------------------+
  | Defaultversion  |       Version        |
  +-----------------+----------------------+
  |  False          |  v1.10.1-eksbuild.6  |
  |  False          |  v1.10.1-eksbuild.5  |
  |  True           |  v1.10.1-eksbuild.2  |
  ...
  +-----------------+----------------------+

#   kube-proxy
aws eks describe-addon-versions --kubernetes-version 1.28 --addon-name kube-proxy \
    --query 'addons[].addonVersions[].{Version: addonVersion, Defaultversion: compatibilities[0].defaultVersion}' --output table
  -------------------------------------------
  |          DescribeAddonVersions          |
  +-----------------+-----------------------+
  | Defaultversion  |        Version        |
  +-----------------+-----------------------+
  |  False          |  v1.28.4-eksbuild.1   |
  |  False          |  v1.28.2-eksbuild.2   |
  |  True           |  v1.28.1-eksbuild.1   |
  ...
  +-----------------+-----------------------+


# Find the configuration options for your chosen add-on by running the following command:
aws eks describe-addon-configuration --addon-name vpc-cni --addon-version v1.14.1-eksbuild.1
aws eks describe-addon-configuration --addon-name coredns --addon-version 1.10.1-eksbuild.2
aws eks describe-addon-configuration --addon-name kube-proxy --addon-version v1.28.1-eksbuild.1

# 1. vpc-cni
# Add-ons prerequisite
#   https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html
#   This add-on utilizes the IAM roles for service accounts capability of Amazon EKS.
#   If your cluster uses the IPv4 family, the permissions in the AmazonEKS_CNI_Policy are required.


# This VPC has two public and two private subnets.
# A public subnet's associated route table has a route to an internet gateway.
# However, the route table of a private subnet doesn't have a route to an internet gateway.

# Pre1) Creating an IAM OIDC provider for a cluster
#   Your cluster has an OpenID Connect (OIDC) issuer URL associated with it.
#   To use AWS Identity and Access Management (IAM) roles for service accounts,
#   an IAM OIDC provider must exist for your cluster's OIDC issuer URL.
#   https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
#   EKS 공식 기능인 "IAM roles for service accounts" 을 추천 합니다.
#   이를 통해 IAM Role을 ServiceAccount와 연관시키고
#   그 ServiceAccount를 Pod과 연결시켜 세분화되고 안전한 권한 부여를 하는 것 입니다.
#   https://emadam.tistory.com/110
#   https://www.blog-dreamus.com/post/flo-tech-aws-eks%EC%97%90%EC%84%9C%EC%9D%98-iam-%EC%97%AD%ED%95%A0-%EB%B6%84%EB%A6%AC

# service account
# https://kubernetes.io/docs/concepts/security/service-accounts/

# ServiceAccount 는 Pod, Service 처럼 K8S 리소스 중 하나이며,
# 사람이 아닌 Pod 와 같은 리소스에 권한(IAM)을 부여하는 역할을 가집니다.
# iam

# aws-load-balancer-controller 역시 ALB 를 생성하는 등의 동작을 하기 위해
# ServiceAccount 가 필요(관련 yaml)합니다. EKS cluster 는 ServiceAccount 에
# IAM role 을 연결(관련 yaml)할 수 있습니다. cluster 가 이렇게 AWS 리소스들과
# 연동하는 경우 AWS 와 일정한 인증 과정이 필요할 것입니다.
# 이러한 연동을 가능하게 하는 것이 OIDC 라는 OAuth 2.0 을 이용해 만들어진 인증 레이어입니다.


cluster_name=my-cluster
echo $cluster_name
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo $oidc_id

# Check if OIDC provider is already in your account
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4

eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve

# Pre2) IAM role with the AmazonEKS_CNI_Policy IAM policy
#   i.e. AmazonEKSVPCCNIRole
#   https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html
#   Prerequisite: create an IAM OIDC provider for your cluster.

#   Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role

# Determine ip Family of your cluster
# "ipFamily": "ipv4"
aws eks describe-cluster --name my-cluster | grep ipFamily

# View OIDC provider url
aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
https://oidc.eks.region-code.amazonaws.com/id/0E9285829A984AEA6C96A20F16C10A84

cat > vpc-cni-trust-policy.json <<-EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::094833749257:oidc-provider/oidc.eks.region-code.amazonaws.com/id/0E9285829A984AEA6C96A20F16C10A84"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.region-code.amazonaws.com/id/0E9285829A984AEA6C96A20F16C10A84:aud": "sts.amazonaws.com",
                    "oidc.eks.region-code.amazonaws.com/id/0E9285829A984AEA6C96A20F16C10A84:sub": "system:serviceaccount:kube-system:aws-node"
                }
            }
        }
    ]
}
EOF


aws iam create-role \
  --role-name AmazonEKSVPCCNIRole \
  --assume-role-policy-document file://"vpc-cni-trust-policy.json"

aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
  --role-name AmazonEKSVPCCNIRole

# annotate the aws-node service account with the ARN of the IAM role
# that you created previously. Replace the example values with your own values.
kubectl annotate serviceaccount \
    -n kube-system aws-node \
    eks.amazonaws.com/role-arn=arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole


#   Step 2: Re-deploy Amazon VPC CNI plugin for KubernetesPods
# Delete and re-create any existing Pods that are associated
# with the service account to apply the credential environment variables.

kubectl delete Pods -n kube-system -l k8s-app=aws-node

kubectl get pods -n kube-system -l k8s-app=aws-node

# replace cpjw7 with the result of the above command
kubectl describe pod -n kube-system aws-node-cpjw7 | grep 'AWS_ROLE_ARN:\|AWS_WEB_IDENTITY_TOKEN_FILE:'

AWS_ROLE_ARN:                 arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole
  AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
  AWS_ROLE_ARN:                           arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole
  AWS_WEB_IDENTITY_TOKEN_FILE:            /var/run/secrets/eks.amazonaws.com/serviceaccount/token


# Step 3: Remove the CNI policy from the node IAM role
aws iam detach-role-policy --role-name myAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy


kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml

aws eks create-addon --cluster-name my-cluster \
  --addon-name vpc-cni --addon-version v1.14.1-eksbuild.1 \
  --service-account-role-arn arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole \
  --configuration-values '{"resources":{"limits":{"cpu":"100m"}}}' \
  --resolve-conflicts OVERWRITE

aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text

aws eks create-addon --cluster-name my-cluster \
  --addon-name coredns --addon-version 1.10.1-eksbuild.2 \
  --service-account-role-arn arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole \
  --configuration-values 'file://example.yaml' \
  --resolve-conflicts OVERWRITE

aws eks create-addon --cluster-name my-cluster \
  --addon-name kube-proxy --addon-version v1.28.1-eksbuild.1 \
  --service-account-role-arn arn:aws:iam::094833749257:role/AmazonEKSVPCCNIRole \
  --configuration-values 'file://example.yaml' \
  --resolve-conflicts OVERWRITE

aws eks list-addons --cluster-name my-cluster

aws eks describe-addon --cluster-name my-cluster \
  --addon-name vpc-cni --query "addon.addonVersion" --output text
```

```tf
resource "aws_eks_addon" "vpc-cni" {
  cluster_name                = aws_eks_cluster.my-cluster.name
  addon_name                  = "vpc-cni"
  addon_version               = "v1.14.1-eksbuild.1"
  resolve_conflicts_on_update = "PRESERVE"
}

resource "aws_eks_addon" "coredns" {
  cluster_name                = aws_eks_cluster.my-cluster.name
  addon_name                  = "coredns"
  addon_version               = "1.10.1-eksbuild.2"
  resolve_conflicts_on_update = "PRESERVE"
}

resource "aws_eks_addon" "kube-proxy" {
  cluster_name                = aws_eks_cluster.my-cluster.name
  addon_name                  = "kube-proxy"
  addon_version               = "v1.28.1-eksbuild.1"
  resolve_conflicts_on_update = "PRESERVE"
}

```

https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html

If an add-on requires IAM permissions, then you must have an IAM OpenID Connect (OIDC) provider for your cluster.


To determine whether you have one, or to create one, see Creating an IAM OIDC provider for your cluster. You can update or delete an add-on once you've installed it.

6. Create nodes

```sh
cat > node-role-trust-policy.json <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the node IAM role
# https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html
aws iam create-role \
  --role-name myAmazonEKSNodeRole \
  --assume-role-policy-document file://"node-role-trust-policy.json"

# Attach the required managed IAM policies to the role
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
  --role-name myAmazonEKSNodeRole
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \ --role-name myAmazonEKSNodeRole
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
  --role-name myAmazonEKSNodeRole
```

- Go to EKS console > cluster > Compute tab
  - Add Node Group: write name and choose Node IAM role name


node (aws-node-wcr6m)

Failed to pull image "602401143452.dkr.ecr.ap-northeast-2.amazonaws.com/amazon/aws-network-policy-agent:v1.0.2-eksbuild.1": failed to pull and unpack image "602401143452.dkr.ecr.ap-northeast-2.amazonaws.com/amazon/aws-network-policy-agent:v1.0.2-eksbuild.1": failed to resolve reference "602401143452.dkr.ecr.ap-northeast-2.amazonaws.com/amazon/aws-network-policy-agent:v1.0.2-eksbuild.1": unexpected status from HEAD request to https://602401143452.dkr.ecr.ap-northeast-2.amazonaws.com/v2/amazon/aws-network-policy-agent/manifests/v1.0.2-eksbuild.1: 401 Unauthorized

Readiness probe failed: {"level":"info","ts":"2024-01-11T14:21:20.132Z","caller":"/root/sdk/go1.20.4/src/runtime/proc.go:250","msg":"timeout: failed to connect service \":50051\" within 5s"}

Back-off restarting failed container aws-node in pod aws-node-wcr6m_kube-system(bd01d52d-8aea-4ef3-adb5-6dee126c63a1)


aws ec2 describe-subnets --region ap-northeast-2 | grep AvailabilityZone\"
            "AvailabilityZone": "ap-northeast-2c",
            "AvailabilityZone": "ap-northeast-2a",
            "AvailabilityZone": "ap-northeast-2b",
            "AvailabilityZone": "ap-northeast-2d",

aws ec2 describe-subnets --region us-east-1 | grep AvailabilityZone\"

private-ap-northeast-2a
private-ap-northeast-2b
public-ap-northeast-2a
public-ap-northeast-2b



- EKS loadbalancer controller

https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.6/

https://three-beans.tistory.com/entry/AWSEKS-%EC%BD%98%EC%86%94%EB%A1%9C-%EC%83%9D%EC%84%B1%ED%95%98%EB%8A%94-EKS-%E2%91%A0-intro-network-%EA%B3%A0%EB%A0%A4%EC%82%AC%ED%95%AD

https://three-beans.tistory.com/entry/AWSEKS-%EC%BD%98%EC%86%94%EB%A1%9C-%EC%83%9D%EC%84%B1%ED%95%98%EB%8A%94-EKS-%E2%91%A3-ingress-AWS-LoadBalancer-Controller-%EA%B5%AC%EC%84%B1

https://velog.io/@holicme7/K8s-EKS-%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C-Istio-ALB-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0-AWS-LoadBalaner-Controller

# Istio + Ingress + ALB + Gateway

https://wrynn.tistory.com/66
https://www.mirantis.com/blog/your-app-deserves-more-than-kubernetes-ingress-kubernetes-ingress-vs-istio-gateway-webinar/
https://rtfm.co.ua/en/aws-elastic-kubernetes-service-running-alb-ingress-controller/
https://journes.tistory.com/60

- 애플리케이션을 외부 사용자가 접근 가능하도록 구성하는 방법에는 여러가지가 있습니다.
  - NodePort 및 LoadBalancer (쿠버네티스 Service)
  - Ingress
  - Istio

- Ingress 구성에서 대표적으로 Nginx가 Ingress controller 역할을 수행한 것과 마찬가지로
- Istio에서는 istio-ingressgateway라고 불리우는 Pod 내부에 포함된 고성능 프록시 컨테이너 Envoy가
- 쿠버네티스 클러스터 내부로 유입되는 트래픽을 가장 먼저 수신하고 각각의 서비스로 라우팅합니다.

- ingress controller
  - https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
  - Istio Ingress is an Istio based ingress controller.
  - https://istio.io/latest/docs/tasks/traffic-management/ingress/kubernetes-ingress/
- ingress
  - https://kubernetes.io/docs/concepts/services-networking/ingress/
  - creating ingress creates alb
  - prerequisite is aws load balancer controller add-on
  - kubernetes.io/ingress.class annotation is required to tell the Istio gateway controller that it should handle this Ingress
- aws load balancer controller add-on
  - https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
  - Kubernetes Ingress
  - Kubernetes service of the LoadBalancer type

- istio ingress gateway
  - https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/

Istio에서 Ingress controller에 대응하는 것이 istio-ingressgateway라면,
규칙을 정의하는 Ingress에 대응하는 것은 Gateway와 Virtual Service라는
쿠버네티스 커스텀 리소스입니다

```
In order for the Ingress resource to work,
the cluster must have an ingress controller running.
Unlike other types of controllers which run as part of the kube-controller-manager binary,
Ingress controllers are not started automatically with a cluster
```

https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
https://velog.io/@holicme7/K8s-EKS-%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C-Istio-ALB-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0-AWS-LoadBalaner-Controller

- Ingress managed LoadBalancer -> Ingress -> Service -> Pod

https://rtfm.co.ua/en/istio-an-overview-and-running-service-mesh-in-kubernetes/
https://rtfm.co.ua/en/istio-external-aws-application-loadbalancer-and-istio-ingress-gateway/

- Traffic flow
  - ALB with SSL
  - EKS cluster
  - EKS worker node
  - Istio Ingress Gateway Service
  - Istio Ingress Gateway Pod
  - Application Service
  - Application Pod

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh


https://sixmen.com/ko/tech/2022-03-31-3-build-eks-cluster-with-terraform/






- https://wrynn.tistory.com/66

# NodePort

NodePort의 경우 노드에 포트를 할당하고, 서비스당 포트를 하나씩 할당한다.
서비스 개수가 늘어나면서, 포트 (기본값: 30000-32767)가 부족할 수 있다.

# Ingress

- NodePort와는 달리 Ingress를 사용하면 노드에 포트를 하나만 사용할 수 있습니다.
쿠버네티스에서 Ingress는 클러스터 내의 서비스에 대한 외부 접근을 관리하는 오브젝트입니다.

운영 환경에서는 노드를 하나만 사용하는 것이 아니므로
로드밸런서를 노드 그룹 앞에 위치시키는 것이 일반적입니다.
로드밸런서와 함께 Ingress를 사용하도록 구성하면
단일 로드밸런서를 진입점으로 하면서,
Ingress의 Host 및 Path 기반 라우팅을 통해 다수의 서비스를 제공할 수 있습니다.

```
Any Pods that are configured to use the service account
can then access any AWS service that the role has permissions to access.
```


# Istio

- Use with EKS

https://nyyang.tistory.com/158
https://dev.to/airoasis/eks-eseo-istio-wa-application-load-balancer-yeongyeol-2k2j
https://sarc.io/index.php/cloud/2282-istio-eks
https://rtfm.co.ua/en/istio-external-aws-application-loadbalancer-and-istio-ingress-gateway/


- Prerequisite: AWS Load Balancer Controller

```
AWS Load Balancer Controller는 Kubernetes에서 YAML 파일을 배포하는 것 만으로
AWS Load Balancer Controller 파드가 이를 감지하여 AWS API를 사용하여
요청한 대로 Load Balancer를 설치 및 구성해주는 오픈소스이다.

Ingress 구성에서 대표적으로 Nginx가 Ingress controller 역할을 수행한 것과
마찬가지로 Istio에서는 istio-ingressgateway라고 불리우는
Pod 내부에 포함된 고성능 프록시 컨테이너 Envoy가 쿠버네티스 클러스터 내부로
유입되는 트래픽을 가장 먼저 수신하고 각각의 서비스로 라우팅합니다.

Istio에서 Ingress controller에 대응하는 것이 istio-ingressgateway라면, 규칙을 정의하는 Ingress에 대응하는 것은 Gateway와 Virtual Service라는 쿠버네티스 커스텀 리소스입니다.
istio-ingressgateway Pod 내부의 Envoy는 Gateway와 Virtual Service에
명시된 규칙대로 트래픽을 라우팅합니다.

```

- Operator로 Istio 설치

istio-operator.yaml

istio labels

```
istio: ingressgateway
istio: ingressgateway-alb
istio: ingressgateway-ext-alb
```

AWS LB (ALB는 Ingress(규칙 명세서)에 의해 생성됨)
-> Istio Service -> Istio Pod
  (여기서 Isito Pod의 Label에 따라서 어떤 Istio Gateway에 정의된
    Rule / Setting 값을 따를 것인지 정하게 된다.)


salat-stage-cwmp.myinfo.net
  myinfo-cwmp-stg-salat

salat-stage-mqtt.myinfo.net
  myinfo-nlb-stage-salat

salat-stage-xmpp.myinfo.net
  myinfo-nlb-stage-salat

salat-stage.myinfo.net
  myinfo-dashboard-stg-salat

```
kubectl label namespace <네임스페이스이름> istio-injection=enabled
```




