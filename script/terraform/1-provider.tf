
# Configure the AWS Provider
provider "aws" {
  profile = local.profile
  region  = local.region
}

# terraform version constraints
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

