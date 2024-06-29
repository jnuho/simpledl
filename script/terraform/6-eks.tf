# specifies which entities (users, services, or accounts) are allowed to assume the role.
# In the context of this .tf, it allows the Amazon EKS service to assume the role;
# attach the required Amazon EKS IAM managed policy to it.

data "aws_iam_policy_document" "cluster-role-assume-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}

# This role is assumed by the EKS control plane to manage the cluster.
# : attach AmazonEKSClusterPolicy to this role

resource "aws_iam_role" "eks_cluster_role" {
  name = "eks-cluster-role"
  assume_role_policy = data.aws_iam_policy_document.cluster-role-assume-policy.json
}

resource "aws_iam_role_policy_attachment" "eks_cluster_role_policy" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_eks_cluster" "my-cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = var.eks_version

  vpc_config {
    subnet_ids = [
      aws_subnet.private-ap-northeast-2a.id,
      aws_subnet.private-ap-northeast-2b.id,
      aws_subnet.public-ap-northeast-2a.id,
      aws_subnet.public-ap-northeast-2b.id
    ]
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_role_policy]
}

# To use some Amazon EKS add-ons(vpc-cni), or to enable individual Kubernetes workloads
# to have specific AWS Identity and Access Management (IAM) permissions,
# create an IAM OpenID Connect (OIDC) provider for your cluster.
# You only need to create an IAM OIDC provider for your cluster once.

# If an add-on(vpc-cni) requires IAM permissions,
# then you must have an IAM OpenID Connect (OIDC) provider for your cluster.

# Create an OIDC provider for the EKS cluster
data "aws_eks_cluster" "my-cluster" {
  name = "my-cluster"
}

data "aws_eks_cluster_auth" "my-cluster" {
  name = data.aws_eks_cluster.my-cluster.name
}

resource "aws_iam_openid_connect_provider" "oidc_provider" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.aws_eks_cluster.my-cluster.certificate_authority[0].data]
  url             = data.aws_eks_cluster.my-cluster.identity[0].oidc[0].issuer
}


# The vpc-cni plugin requires you to attach the following IAM policies to an IAM role:
# AmazonEKS_CNI_Policy

data "aws_iam_policy_document" "vpc_cni_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}

# This role is specifically for the VPC CNI add-on, which handles networking for the EKS cluster.
# : attach AmazonEKS_CNI_Policy to this role

resource "aws_iam_role" "eks_cni_role" {
  name = "eks-cni-role"
  assume_role_policy = data.aws_iam_policy_document.vpc_cni_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "eks_cni_role_policy" {
  role       = aws_iam_role.eks_cni_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_eks_addon" "addons" {
  for_each                = { for addon in var.addons : addon.name => addon }
  cluster_name            = aws_eks_cluster.my-cluster.name
  addon_name              = each.value.name
  addon_version           = each.value.version
  resolve_conflicts_on_update = "OVERWRITE"

  dynamic "provider" {
    for_each = each.value.name == "vpc-cni" ? [1] : []
    content {
      service_account_role_arn = aws_iam_role.eks_cni_role.arn
    }
  }
}