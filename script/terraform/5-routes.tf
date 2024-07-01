
# public route table
resource "aws_route_table" "public_rtb" {
  vpc_id = aws_vpc.main.id

  route {
    # the CIDR block of the route
    cidr_block                 = "0.0.0.0/0"

    # identifier of a VPC internet gateway or a virtual private gateway
    gateway_id                 = aws_internet_gateway.main.id
  }
  
  # a map of tags to assign to the resource
  tags = {
    Name = "public rtb"
  }
}


/* Private route tables route traffic through NAT gateways,
 * while the public route table routes traffic through an Internet gateway.
 */

// private route table 01
resource "aws_route_table" "private_rtb_01" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block                 = "0.0.0.0/0"

    # identifier of a VPC NAT gateway
    nat_gateway_id             = aws_nat_gateway.nat_gw_01.id
  }

  tags = {
    Name = "private rtb 01"
  }
}

// private route table 02
resource "aws_route_table" "private_rtb_02" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block                 = "0.0.0.0/0"

    # identifier of a VPC NAT gateway
    nat_gateway_id             = aws_nat_gateway.nat_gw_02.id
  }

  tags = {
    Name = "private rtb 02"
  }
}

resource "aws_route_table_association" "public_rtb_asso_01" {
  # subnet id to create an association
  subnet_id      = aws_subnet.public_1.id

  # id of the routing table to associate with
  route_table_id = aws_route_table.public_rtb.id
}

resource "aws_route_table_association" "public_rtb_asso_02" {
  # subnet id to create an association
  subnet_id      = aws_subnet.public_2.id

  # id of the routing table to associate with
  route_table_id = aws_route_table.public_rtb.id
}

resource "aws_route_table_association" "private_rtb_asso_01" {
  # subnet id to create an association
  subnet_id      = aws_subnet.private_1.id

  # id of the routing table to associate with
  route_table_id = aws_route_table.private_rtb_01.id
}

resource "aws_route_table_association" "private_rtb_asso_02" {
  # subnet id to create an association
  subnet_id      = aws_subnet.private_2.id

  # id of the routing table to associate with
  route_table_id = aws_route_table.private_rtb_02.id
}
