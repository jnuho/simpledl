# manage permissions to applications attach policies to node directly pod will also have same permissions
# >>> OR create OIDC provider which will allow granting IAM permissions based on the serviceaccount used by the pod.

# Create an OIDC provider for the EKS cluster

data "tls_certificate" "eks_cluster_ca" {
  url = data.aws_eks_cluster.my-cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "oidc_provider" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks_cluster_ca.certificates[0].sha1_fingerprint]
  url             = data.aws_eks_cluster.my-cluster.identity[0].oidc[0].issuer
}
