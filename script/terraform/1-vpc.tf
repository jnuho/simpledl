// vpc
resource "aws_vpc" "vpc" {
  cidr_block           = "172.16.0.0/16"

  // Enables DNS hostnames for instances in the VPC
  // instances will receive DNS hostnames that can be resolved to their private IP addresses.

  //enable_dns_hostnames = true     

  tags = {
    "Name" = "vpc"
  }
}

