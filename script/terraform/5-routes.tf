
// private route table 01
resource "aws_route_table" "private_rtb_01" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block                 = "0.0.0.0/0"
    nat_gateway_id             = aws_nat_gateway.nat_gw_01.id
  }

  tags = {
    Name = "Private rtb 01"
  }
}

// private route table 02
resource "aws_route_table" "private_rtb_02" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block                 = "0.0.0.0/0"
    nat_gateway_id             = aws_nat_gateway.nat_gw_02.id
  }

  tags = {
    Name = "Private rtb 02"
  }
}

// public route table
resource "aws_route_table" "public_rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block                 = "0.0.0.0/0"
    gateway_id                 = aws_internet_gateway.igw.id
  }
  
  tags = {
    Name = "Public rtb"
  }
}

//resource "aws_route" "private_rtb" {
//  route_table_id         = aws_route_table.private_rtb.id
//  destination_cidr_block = "0.0.0.0/0"
//  nat_gateway_id         = aws_nat_gateway.nat_gw.id
//}
//resource "aws_route" "public_rtb" {
//  route_table_id         = aws_route_table.public_rtb.id
//  destination_cidr_block = "0.0.0.0/0"
//  gateway_id             = aws_internet_gateway.igw.id
//}

resource "aws_route_table_association" "private_rtb_asso_01" {
  subnet_id      = aws_subnet.private-ap-northeast-2a.id
  route_table_id = aws_route_table.private_rtb_01.id
}

resource "aws_route_table_association" "private_rtb_asso_02" {
  subnet_id      = aws_subnet.private-ap-northeast-2b.id
  route_table_id = aws_route_table.private_rtb_02.id
}

resource "aws_route_table_association" "public_rtb_asso_01" {
  subnet_id      = aws_subnet.public-ap-northeast-2a.id
  route_table_id = aws_route_table.public_rtb.id
}

resource "aws_route_table_association" "public_rtb_asso_02" {
  subnet_id      = aws_subnet.public-ap-northeast-2b.id
  route_table_id = aws_route_table.public_rtb.id
}

