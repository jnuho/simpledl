variable "eks_version" {
  description = "EKS version to use for the cluster"
  type        = string
  default     = "1.21" # specify the default EKS version
}

variable "vpc_cni_version" {
  description = "Version of the VPC CNI add-on"
  type        = string
  default     = "v1.7.5" # specify the default VPC CNI version
}

variable "coredns_version" {
  description = "Version of the CoreDNS add-on"
  type        = string
  default     = "v1.8.0" # specify the default CoreDNS version
}

variable "kube_proxy_version" {
  description = "Version of the KubeProxy add-on"
  type        = string
  default     = "v1.7.8" # specify the default KubeProxy version
}