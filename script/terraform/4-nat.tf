
// EIP for NAT gw
// 출발지 Private Subnet EC2 <--> NAT Gateway(EIP) ----  인터넷 ---- 목적지 타사 도메인 또는 Public IP <--> 타사 서버
resource "aws_eip" "nat_eip_01" {
  domain   = "vpc"
}

resource "aws_eip" "nat_eip_02" {
  domain   = "vpc"
}

// NAT gateway
resource "aws_nat_gateway" "nat_gw_01" {
  allocation_id = aws_eip.nat_eip_01.id
  subnet_id     = aws_subnet.public-ap-northeast-2a.id

  depends_on = [
    aws_internet_gateway.igw,
  ]
}

resource "aws_nat_gateway" "nat_gw_02" {
  allocation_id = aws_eip.nat_eip_02.id
  subnet_id     = aws_subnet.public-ap-northeast-2b.id

  depends_on = [
    aws_internet_gateway.igw,
  ]
}
