
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

resource "aws_iam_role" "my-role" {
  name = "my-cluster-role"
  assume_role_policy = data.aws_iam_policy_document.cluster-role-assume-policy.json
}

resource "aws_iam_role_policy_attachment" "my-cluster-role-policy" {
  role       = aws_iam_role.my-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
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


resource "aws_eks_addon" "addons" {
  for_each                = { for addon in var.addons : addon.name => addon }
  cluster_name            = aws_eks_cluster.my-cluster.name
  addon_name              = each.value.name
  addon_version           = each.value.version
  resolve_conflicts_on_update = "OVERWRITE"

  provider {
    if each.value.name == "vpc-cni" {
      service_account_role_arn = aws_iam_role.eks_cni_role.arn
    }
  }
}