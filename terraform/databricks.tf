# Define a Schema within the Catalog
resource "databricks_schema" "zoopla" {
  catalog_name = "houseful"
  name = "zoopla"
}

data "databricks_spark_version" "latest" {
  latest = true
}

resource "databricks_secret_scope" "aws_s3_access" {
  name = "aws-s3-access"
}

resource "databricks_secret" "aws_access_key" {
  key          = "aws-access-key-id"
  string_value = var.aws_access_key_id
  scope        = databricks_secret_scope.aws_s3_access.name
}

resource "databricks_secret" "aws_secret_key" {
  key          = "aws-secret-access-key"
  string_value = var.aws_secret_access_key
  scope        = databricks_secret_scope.aws_s3_access.name
}
