variable "project_name" {
  type        = map
  description = "Name of the project."
  default     = {
    dev  = "davemike-dev"
    prod = "davemike-prod"
  }
}

variable "env" {
  description = "env: dev or prod"
}

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

variable "aws_backup_bucket_name" {
    description = "The name of the bucket to backup the db"
}

variable "key_name" {
  type = string
  description = "Name of the private key"
}


