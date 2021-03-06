

provider "aws" {
    profile     = "default"
    region     = var.aws_s3_region_name
    version = "~> 3.10"
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
}

######## EC2 ############

resource "aws_instance" "webserver" {
    ami                  = "ami-0e82959d4ed12de3f"
    instance_type        = "t2.micro"
    key_name             = var.key_name
    iam_instance_profile = aws_iam_instance_profile.ec2_s3_profile.name
    security_groups      = [aws_security_group.davemike_allow_http_ssh.name]
    # user_data            = file("./provision.sh")
    tags = {
        Name = "Sandbox"
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
  bucket = var.aws_storage_bucket_name
  acl    = "private"
  tags = {
    Name        = "Sandbox Bucket"
    Environment = "Dev"
  }
}

######## Security Group ############

resource "aws_security_group" "davemike_allow_http_ssh" {
  name        = "davemike_allow_http_ssh"
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
  name = "ec2_s3_role" 
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
  name = "ec2_s3_profile"
  role = aws_iam_role.ec2_s3_role.name
}


resource "aws_iam_role_policy" "ec2_s3_policy" {
  name = "ec2_s3_policy"
  role = aws_iam_role.ec2_s3_role.id
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
                "arn:aws:s3:::${var.aws_storage_bucket_name}/*"
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
