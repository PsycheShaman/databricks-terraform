resource "databricks_schema" "sales_and_rentals_bronze" {
  catalog_name = "real_estate_inc"
  name         = "sales_and_rentals_bronze"
}

resource "databricks_schema" "sales_and_rentals_silver" {
  catalog_name = "real_estate_inc"
  name         = "sales_and_rentals_silver"
}

resource "databricks_schema" "sales_and_rentals_gold" {
  catalog_name = "real_estate_inc"
  name         = "sales_and_rentals_gold"
}