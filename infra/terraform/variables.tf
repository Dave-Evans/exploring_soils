variable "region" {
    default = "us-east-2"
}

variable "aws_access_key" {
    description = "AWS Access Key"
}

variable "aws_secret_key" {
    description = "AWS Access Key"
}

variable "bucketname" {
    description = "The name of the primary app bucket"
}

variable "image_id" {
  type = string
  description = "The id of the AMI"
}

variable "key_name" {
  type = string
  description = "Name of the private key"
}

