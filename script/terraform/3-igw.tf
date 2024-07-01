
// internet gateway
// is required for an Amazon EKS cluster for worker nodes (EC2) to have internet access
// 1. Pulling container images from public repositories.
// 2. Communicating with the EKS control plane.
// 3. Accessing other AWS services and updates.
// Without an Internet Gateway, your EKS cluster nodes would not be able to
// communicate with the internet unless you set up a NAT Gateway or NAT instance for private subnets.

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.env}-igw"
  }
}

