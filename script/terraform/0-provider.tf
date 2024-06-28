
# Configure the AWS Provider
provider "aws" {
  region = "ap-northeast-2"
  profile = "default"
}

# 가용역역
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones
# Define a data source to fetch available AWS availability zones

data "aws_availability_zones" "available" {
  state = "available"
}
