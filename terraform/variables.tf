# variables.tf

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "s3_bucket" {
  description = "S3 bucket for storing listings"
  type        = string
  default     = "sales_and_rentals-raw"
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

variable "lambda_exec_role_id" {
  type      = string
  sensitive = true
}

variable "lambda_exec_role_name" {
  type      = string
  sensitive = true
}

variable "git_url" {
  description = "URL of the Git repository"
  type        = string
  default     = "https://github.com/PsycheShaman/houseful-technical-interview.git"
}

variable "git_branch" {
  description = "Branch of the Git repository"
  type        = string
  default     = "main"
}

variable "git_personal_access_token" {
  description = "Personal access token for the Git repository"
  type        = string
  sensitive   = true
}

variable "git_username" {
  type    = string
  default = "PsycheShaman"
}

variable "aws_access_key_id" {
  type      = string
  sensitive = true
}

variable "aws_secret_access_key" {
  type      = string
  sensitive = true
}

variable "workspace_id" {
  type    = string
  default = "2905500365526979"
}