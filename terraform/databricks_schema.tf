resource "databricks_schema" "zoopla_bronze" {
  catalog_name = "houseful"
  name         = "zoopla_bronze"
}

resource "databricks_schema" "zoopla_silver" {
  catalog_name = "houseful"
  name         = "zoopla_silver"
}

resource "databricks_schema" "zoopla_gold" {
  catalog_name = "houseful"
  name         = "zoopla_gold"
}