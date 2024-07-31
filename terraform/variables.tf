# variables.tf

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
