locals {
  env         = "dev"
  profile     = "terraform"
  region      = "ap-northeast-2"
  zone1       = "ap-northeast-2a"
  zone2       = "ap-northeast-2b"
  eks_name    = "my-cluster"
  eks_version = "1.30"
}

variable "addons" {
  type = list(object({
    name    = string
    version = string
  }))
  default = [
    {
      name    = "vpc-cni"
      version = "v1.18.2-eksbuild.1"
    },
    {
      name    = "coredns"
      version = "v1.11.1-eksbuild.9"
    },
    {
      name    = "kube-proxy"
      version = "v1.30.0-eksbuild.3",
    },
    //{
    //  name    = "aws-ebs-csi-driver"
    //  version = "v1.25.0-eksbuild.1"
    //}
  ]
}