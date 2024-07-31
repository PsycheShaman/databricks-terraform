# variables.tf

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "s3_bucket" {
  description = "S3 bucket for storing listings"
  type        = string
  default     = "z-raw"
}

variable "databricks_host" {
  description = "Databricks instance URL"
  type        = string
  sensitive   = true
}

variable "databricks_client_id" {
  description = "Databricks client ID"
  type        = string
  sensitive   = true
}

variable "databricks_client_secret" {
  description = "Databricks client secret"
  type        = string
  sensitive   = true
}
