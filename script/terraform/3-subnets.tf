# 가용역역
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones
# Define a data source to fetch available AWS availability zones
# data "aws_availability_zones" "available" {
#   state = "available"
# }

# public subnet01
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "172.16.0.0/18"
  availability_zone       = "ap-northeast-2a"

  # Required for EKS. Instances in this subnet will be assigned a public IP
  map_public_ip_on_launch = true

  tags = {
    Name                        = "public-ap-northeast-2a"
    # Required for EKS.
    # subnet is shared with the EKS cluster.
    "kubernetes.io/cluster/my-cluster" = "shared"
    # subnet can be used for external load balancers.
    "kubernetes.io/role/elb"    = "1"
  }
}

# public subnet02
resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "172.16.64.0/18"
  availability_zone       = "ap-northeast-2b"

  # Required for EKS. Instances in this subnet will be assigned a public IP
  map_public_ip_on_launch = true

  tags = {
    Name                        = "public-ap-northeast-2b"
    # Required for EKS.
    # subnet is shared with the EKS cluster.
    "kubernetes.io/cluster/my-cluster" = "shared"
    # subnet can be used for external load balancers.
    "kubernetes.io/role/elb"    = "1"
  }
}


# private subnets01
resource "aws_subnet" "private_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              =  "172.16.128.0/18"
  availability_zone       = "ap-northeast-2a"
  tags = {
    Name                              = "private-ap-northeast-2a"
    # Required for EKS.
    # subnet is shared with the EKS cluster.
    "kubernetes.io/cluster/my-cluster" = "shared"
    # subnet can be used for internal private load balancers.
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# private subnets02
resource "aws_subnet" "private_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "172.16.192.0/18"
  availability_zone       = "ap-northeast-2b"
  tags = {
    Name                              = "private-ap-northeast-2b"
    # Required for EKS.
    # subnet is shared with the EKS cluster.
    "kubernetes.io/cluster/my-cluster" = "shared"
    # subnet can be used for internal privateload balancers.
    "kubernetes.io/role/internal-elb" = "1"
  }
}


