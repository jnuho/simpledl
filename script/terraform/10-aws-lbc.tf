
data "aws_iam_policy_document" "aws-lbc-assume-policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      # for IAM role to be used only by EKS services
      identifiers = ["pods.eks.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
      "sts:TagSession"
    ]
  }
}
# This role is assumed by the EKS control plane to manage the cluster.
resource "aws_iam_role" "aws-lbc" {
  name = "aws-lbc"
  assume_role_policy = data.aws_iam_policy_document.aws-lbc-assume-policy.json
}

resource "aws_iam_policy" "aws-lbc" {
  policy = file("./iam/AWSLoadBalancerController.json")
  name   = "AWSLoadBalancerControllerPolicy"
}

resource "aws_iam_role_policy_attachment" "aws-lbc" {
  role       = aws_iam_role.aws-lbc.name
  policy_arn = aws_iam_policy.aws-lbc.arn
}

resource "aws_eks_pod_identity_association" "aws-lbc" {
  cluster_name = aws_eks_cluster.my-cluster.name
  namespace = "kube-system"
  service_account = "aws-load-balancer-controller"
  role_arn = aws_iam_role.aws-lbc.arn
}

resource "helm_release" "aws-lbc" {
  name = "aws-load-balancer-controller"

  repository = "https://aws.github.io/eks-charts"
  chart       = "aws-load-balancer-controller"
  namespace   = "kube-system"
  version     = "1.7.2"

  set {
    name  = "clusterName"
    value = aws_eks_cluster.my-cluster.name
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  # depends_on = [helm_release.cluster_autoscaler]
}