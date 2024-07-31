# main.tf

terraform {
  backend "s3" {
    bucket = "z-raw"
    key    = "terraform/state"
    region = "eu-west-1"
  }
}

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
      version = "1.49.1"
    }
  }
}

provider "databricks" {
  host          = var.databricks_host
  client_id     = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

