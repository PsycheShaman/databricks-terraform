# Define a Schema within the Catalog
resource "databricks_schema" "zoopla" {
  catalog_name = "houseful"
  name = "zoopla"
}