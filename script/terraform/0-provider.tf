
# Configure the AWS Provider
provider "aws" {
  profile = "terraform"
  region = "ap-northeast-2"
}

# terraform version constraints
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

