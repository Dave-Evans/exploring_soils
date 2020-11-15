variable "aws_s3_region_name" {
    default = "us-east-2"
}

variable "aws_access_key_id" {
    description = "AWS Access Key"
}

variable "aws_secret_access_key" {
    description = "AWS Access Key"
}

variable "aws_storage_bucket_name" {
    description = "The name of the primary app bucket"
}

variable "key_name" {
  type = string
  description = "Name of the private key"
}

