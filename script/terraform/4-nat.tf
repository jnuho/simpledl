
// EIP for NAT gw
// 출발지 Private Subnet EC2 <--> NAT Gateway(EIP) ----  인터넷 ---- 목적지 타사 도메인 또는 Public IP <--> 타사 서버

# An Elastic IP address is a static IPv4 address designed for dynamic cloud computing. By using an Elastic IP address, you can 
# associate it with an instance in a VPC and have the address remain fixed even if the instance is stopped or terminated.
# This is useful for applications that require a static IP address for outbound connections.

# Two NAT gateways and Eips in case of 1 of the availability zone is down for high availability!

resource "aws_eip" "nat_eip_01" {
  # Indicates if this EIP is for use in VPC (vpc).
  domain   = "vpc"

  # EIP may require IGW to be created first
  # Use depends_on to set an explicit dependency on the IGW.
  depends_on = [ aws_internet_gateway.main ]
}

resource "aws_eip" "nat_eip_02" {
  # Indicates if this EIP is for use in VPC (vpc).
  domain   = "vpc"

  # EIP may require IGW to be created first
  # Use depends_on to set an explicit dependency on the IGW.
  depends_on = [ aws_internet_gateway.main ]
}

// NAT gateway
resource "aws_nat_gateway" "nat_gw_01" {
  # allocation id of the EIP address for the gateway
  allocation_id = aws_eip.nat_eip_01.id

  # subnet id of the public subnet in which to place the gateway
  subnet_id     = aws_subnet.public_1.id

  tags = {
    Name = "NAT GW 1"
  }

  depends_on = [
    aws_internet_gateway.main,
  ]
}

resource "aws_nat_gateway" "nat_gw_02" {
  # allocation id of the EIP address for the gateway
  allocation_id = aws_eip.nat_eip_02.id

  # subnet id of the public subnet in which to place the gateway
  subnet_id     = aws_subnet.public_2.id

  tags = {
    Name = "NAT GW 2"
  }

  depends_on = [
    aws_internet_gateway.main,
  ]
}
