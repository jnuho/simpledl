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

# Security Group

resource "aws_security_group" "eks_cluster_sg" {
  name        = "eks-cluster-sg"
  description = "Security group for EKS cluster"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-cluster-sg"
  }
}

resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["xx.xx.xx.xx/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}

resource "aws_eks_cluster" "my-cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = var.eks_version

  vpc_config {
    subnet_ids = [
      aws_subnet.private_1.id,
      aws_subnet.private_2.id,
      aws_subnet.public_1.id,
      aws_subnet.public_2.id
    ]
    security_group_ids = [aws_security_group.eks_cluster_sg.id]
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_role_policy]
}

# To use some Amazon EKS add-ons(vpc-cni), or to enable individual Kubernetes workloads
# to have specific AWS Identity and Access Management (IAM) permissions,
# create an IAM OpenID Connect (OIDC) provider for your cluster.
# You only need to create an IAM OIDC provider for your cluster once.

# If an add-on(vpc-cni) requires IAM permissions,
# then you must have an IAM OpenID Connect (OIDC) provider for your cluster.


# Ensure the EKS cluster is created before reading its data

# data "aws_eks_cluster" "my-cluster" {
#   name = aws_eks_cluster.my-cluster.name
#   depends_on = [aws_eks_cluster.my-cluster]
# }

# Create an OIDC provider for the EKS cluster

# data "tls_certificate" "eks_cluster_ca" {
#   url = data.aws_eks_cluster.my-cluster.certificate_authority[0].data
# }

# resource "aws_iam_openid_connect_provider" "oidc_provider" {
#   client_id_list  = ["sts.amazonaws.com"]
#   thumbprint_list = [data.tls_certificate.eks_cluster_ca.certificates[0].sha1_fingerprint]
#   url             = data.aws_eks_cluster.my-cluster.identity[0].oidc[0].issuer
# }

# The vpc-cni plugin requires you to attach the following IAM policies to an IAM role:
# AmazonEKS_CNI_Policy

# data "aws_iam_policy_document" "vpc_cni_assume_role_policy" {
#   statement {
#     actions = ["sts:AssumeRole"]

#     principals {
#       type        = "Service"
#       identifiers = ["eks.amazonaws.com"]
#     }
#   }
# }

# This role is specifically for the VPC CNI add-on, which handles networking for the EKS cluster.
# : attach AmazonEKS_CNI_Policy to this role

# resource "aws_iam_role" "eks_cni_role" {
#   name = "eks-cni-role"
#   assume_role_policy = data.aws_iam_policy_document.vpc_cni_assume_role_policy.json
# }

# resource "aws_iam_role_policy_attachment" "eks_cni_role_policy" {
#   role       = aws_iam_role.eks_cni_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
# }


# resource "aws_eks_addon" "addons" {
#   for_each                = { for addon in var.addons : addon.name => addon }
#   cluster_name            = aws_eks_cluster.my-cluster.name
#   addon_name              = each.value.name
#   addon_version           = each.value.version
#   resolve_conflicts_on_update = "OVERWRITE"

#   service_account_role_arn = each.value.name == "vpc-cni" ? aws_iam_role.eks_cni_role.arn : null
# }