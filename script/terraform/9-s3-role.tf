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

resource "aws_iam_role" "test-oidc-s3-role" {
  assume_role_policy = data.aws_iam_policy_document.test_oidc_assume_role_policy.json
  name               = "test-oidc-s3-role"
}

resource "aws_iam_policy" "test-policy-s3" {
  name = "test-policy-s3"

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
  role       = aws_iam_role.test-oidc-s3-role.name
  policy_arn = aws_iam_policy.test-policy-s3.arn
}

output "test_policy_arn" {
  value = aws_iam_role.test-oidc-s3-role.arn
}


