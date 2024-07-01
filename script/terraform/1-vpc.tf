// vpc
resource "aws_vpc" "main" {
  # CIDR block for the VPC
  cidr_block           = "172.16.0.0/16"

  # Enables DNS hostnames for instances in the VPC
  # instances will receive DNS hostnames that can be resolved to their private IP addresses.


  # Makes your instances run in a shared tenancy by default
  instance_tenancy = "default"

  # Required for EKS. Enables DNS support for the VPC
  enable_dns_support = true

  # Required for EKS. Enables DNS hostnames for instances in the VPC
  enable_dns_hostnames = true     

  # Requests an IPv6 CIDR block with a /56 prefix length
  assign_generated_ipv6_cidr_block = false

  tags = {
    "Name" = "main"
  }
}

# output "vpc_id" {
#   value = aws_vpc.main.id
#   description = "VPC id."
#   # Setting an output value as sensitive will mask it in the console output
#   sensitive = false
# }
