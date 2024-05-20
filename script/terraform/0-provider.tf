
# Configure the AWS Provider
provider "aws" {
  region = "ap-northeast-2"
  access_key = "ACCES_KEY"
  secret_key = "SECRET_KEY"
}

# 가용역역
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones
data "aws_availability_zones" "available" {
  state = "available"
}

# EC2 Amazon Linux 2
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}
