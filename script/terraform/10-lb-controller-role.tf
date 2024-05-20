
# Create role for load balancer controller
resource "aws_iam_role" "lb-controller-role" {
  assume_role_policy = data.aws_iam_policy_document.test_oidc_assume_role_policy.json
  name               = "lb-controller-role"
}

# Create policy
data "http" "iam_policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json"
}

resource "aws_iam_policy" "lb-controller-policy" {
  name = "test-policy"
  policy      = data.http.iam_policy.response_body
}

resource "aws_iam_role_policy_attachment" "lb-controller-attach" {
  role       = aws_iam_role.lb-controller-role.name
  policy_arn = aws_iam_policy.lb-controller-policy.arn
}

