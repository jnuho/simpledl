
resource "aws_iam_role" "my-role" {
  name = "my-cluster-role"

# specifies which entities (users, services, or accounts) are allowed to assume the role.
# In the context of this .tf, it allows the Amazon EKS service to assume the role;
# attach the required Amazon EKS IAM managed policy to it.

  assume_role_policy = <<POLICY
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
POLICY
}

resource "aws_iam_role_policy_attachment" "my-cluster-role-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.my-role.name
}

resource "aws_eks_cluster" "my-cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.my-role.arn
  version  = var.eks_version

  vpc_config {
    subnet_ids = [
      aws_subnet.private-ap-northeast-2a.id,
      aws_subnet.private-ap-northeast-2b.id,
      aws_subnet.public-ap-northeast-2a.id,
      aws_subnet.public-ap-northeast-2b.id
    ]
  }

  depends_on = [aws_iam_role_policy_attachment.my-cluster-role-policy]
}


// If an add-on requires IAM permissions,
// then you must have an IAM OpenID Connect (OIDC) provider for your cluster. 

resource "aws_eks_addon" "vpc_cni" {
  cluster_name     = aws_eks_cluster.my-cluster.name
  addon_name       = "vpc-cni"
  addon_version    = var.vpc_cni_version
  resolve_conflicts = "OVERWRITE"
}

resource "aws_eks_addon" "coredns" {
  cluster_name     = aws_eks_cluster.my-cluster.name
  addon_name       = "coredns"
  addon_version    = var.coredns_version
  resolve_conflicts = "OVERWRITE"
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name     = aws_eks_cluster.my-cluster.name
  addon_name       = "kube-proxy"
  addon_version    = var.kube_proxy_version
  resolve_conflicts = "OVERWRITE"
}