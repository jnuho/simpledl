
# Amazon EKS node IAM role
# https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html

# Subject to "ec2.amazonaws.com"

data "aws_iam_policy_document" "nodes_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      # for IAM role to be used only by EC2 services
      identifiers = ["ec2.amazonaws.com"]
    }
    effect = "Allow"
  }
}
resource "aws_iam_role" "nodes" {
  name               = "eks-node-group-nodes"
  assume_role_policy = data.aws_iam_policy_document.nodes_assume_role_policy.json
}

# https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html
resource "aws_iam_role_policy_attachment" "nodes_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.nodes.name
}

# https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html
resource "aws_iam_role_policy_attachment" "nodes_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.nodes.name
}

# https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEC2ContainerRegistryReadOnly.html
resource "aws_iam_role_policy_attachment" "nodes_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.nodes.name
}

# Ensure that your nodes have the necessary security group rules to allow traffic.

# resource "aws_security_group" "eks_node_group_sg" {
#   name        = "eks-node-group-sg"
#   description = "Security group for EKS node group"
#   vpc_id      = aws_vpc.main.id

#   ingress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

resource "aws_eks_node_group" "private_nodes" {
  cluster_name    = aws_eks_cluster.my-cluster.name
  version         = local.eks_version
  node_group_name = "private-nodes"
  node_role_arn   = aws_iam_role.nodes.arn

  subnet_ids = [
    aws_subnet.private_zone1.id,
    aws_subnet.private_zone2.id
  ]

  capacity_type  = "ON_DEMAND"
  instance_types = ["t3.medium"]

  # disk_size = 30

  # Creates EC2 Auto Scaling Group
  scaling_config {
    desired_size = 1
    max_size     = 5
    min_size     = 0
  }

  update_config {
    max_unavailable = 1
  }

  # NOTE:
  # You can use labels to instruct kubernetes scheduler to use
  # a perticular node group by using affinity or node selector
  # Speicfy deployment object to only create pods in node groups with role="general"
  labels = {
    role = "general"
  }

  # taint {
  #   key    = "team"
  #   value  = "devops"
  #   effect = "NO_SCHEDULE"
  # }

  # launch_template {
  #   name    = aws_launch_template.eks_with_disks.name
  #   version = aws_launch_template.eks_with_disks.latest_version
  # }

  depends_on = [
    aws_iam_role_policy_attachment.nodes_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.nodes_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.nodes_AmazonEC2ContainerRegistryReadOnly,
  ]

  # Allow external changes without Terraform plan difference
  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}

# resource "aws_launch_template" "eks_with_disks" {
#   name = "eks-with-disks"

#   key_name = "local-provisioner"

#   block_device_mappings {
#     device_name = "/dev/xvdb"

#     ebs {
#       volume_size = 50
#       volume_type = "gp2"
#     }
#   }
# }