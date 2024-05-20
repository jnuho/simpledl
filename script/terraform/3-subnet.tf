# private subnets01
resource "aws_subnet" "private-ap-northeast-2a" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block              = "172.16.0.0/18"
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name = "Private Subnet01"
    kubernetes.io/role/internal-elb = "1"
  }
}

# private subnets02
resource "aws_subnet" "private-ap-northeast-2b" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block              = "172.16.64.0/18"
  availability_zone = data.aws_availability_zones.available.names[1]
  tags = {
    Name = "Private Subnet02"
    kubernetes.io/role/internal-elb = "1"
  }
}


# public subnet01
resource "aws_subnet" "public-ap-northeast-2a" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block        = "172.16.128.0/18"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet01"
    kubernetes.io/role/elb = "1"
  }
}

# public subnet02
resource "aws_subnet" "public-ap-northeast-2b" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block        = "172.16.192.0/18"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet02"
    kubernetes.io/role/elb = "1"
  }
}

