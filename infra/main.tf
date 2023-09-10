

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  profile    = "default"
  region     = var.aws_s3_region_name
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

######## EC2 ############

resource "aws_instance" "webserver" {
  ami                  = "ami-0fb653ca2d3203ac1"
  instance_type        = "t3a.micro"
  key_name             = var.key_name
  iam_instance_profile = aws_iam_instance_profile.ec2_s3_profile.name
  security_groups      = [aws_security_group.davemike_allow_http_ssh.name]
  # user_data            = file("./provision.sh")
  tags = {
    Name = "webserver-${lookup(var.project_name, var.env)}"
  }

}

######## Elastic IP ########

# resource "aws_eip" "elastic_ip" {
#   instance = aws_instance.webserver.id
#   vpc      = true
#   tags = {
#     Name = "Sandbox Permanent IP"
#   } 
# }

######## S3 ############

resource "aws_s3_bucket" "greencover_sandbox" {
  # bucket = var.aws_storage_bucket_name
  bucket = var.aws_storage_bucket_name
  acl    = "private"
  tags = {
    Name        = "Bucket for storage"
    Environment = var.env
  }
}

######## Security Group ############

resource "aws_security_group" "davemike_allow_http_ssh" {
  name        = "davemike_allow_http_ssh_${var.env}"
  description = "Allow HTTP in and out and SSH in"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # cidr_blocks = ["207.153.46.73/0"]
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http_ssh"
  }
}


######## Role, Policy, Instance Profile ############

resource "aws_iam_role" "ec2_s3_role" {
  name               = "ec2_s3_role_${var.env}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "ec2_s3_profile_${var.env}"
  role = aws_iam_role.ec2_s3_role.name
}


resource "aws_iam_role_policy" "ec2_s3_policy" {
  name   = "ec2_s3_policy_${var.env}"
  role   = aws_iam_role.ec2_s3_role.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Action": [
            "s3:PutObject",
            "s3:PutObjectAcl",
            "s3:GetObject",
            "s3:GetObjectAcl",
            "s3:GetBucketTagging",
            "s3:ListBucket",
            "s3:GetBucketVersioning",
            "s3:DeleteObject",
            "s3:GetBucketLocation"
        ],
      "Effect": "Allow",
      "Resource": [
                "arn:aws:s3:::${var.aws_storage_bucket_name}",
                "arn:aws:s3:::${var.aws_storage_bucket_name}/*",
                "arn:aws:s3:::${var.aws_backup_bucket_name}",
                "arn:aws:s3:::${var.aws_backup_bucket_name}/*"                
            ]
    }
  ]
}
EOF
}


######## Output ############

output "ip" {
  value = aws_instance.webserver.public_ip
}

output "webserver-instance-id" {
  value = aws_instance.webserver.id
}
