# data "databricks_current_user" "me" {}

# resource "databricks_metastore" "uc_metastore" {
#   name = "houseful_unity_catalog"
# }

# resource "databricks_metastore_assignment" "assign_uc_metastore" {
#   metastore_id         = databricks_metastore.uc_metastore.id
#   workspace_id         = var.workspace_id
#   default_catalog_name = "main"
# }

# resource "databricks_catalog" "uc_catalog" {
#   name         = "zoopla"
#   metastore_id = databricks_metastore.uc_metastore.id
# }

# resource "databricks_schema" "bronze_schema" {
#   name         = "bronze"
#   catalog_name = databricks_catalog.uc_catalog.name
# }

# resource "databricks_schema" "silver_schema" {
#   name         = "silver"
#   catalog_name = databricks_catalog.uc_catalog.name
# }

# resource "databricks_schema" "gold_schema" {
#   name         = "gold"
#   catalog_name = databricks_catalog.uc_catalog.name
# }

# resource "databricks_schema" "gold_scd2_schema" {
#   name         = "gold_scd2"
#   catalog_name = databricks_catalog.uc_catalog.name
# }


# resource "databricks_grants" "bronze_schema_permissions" {
#   schema = "${databricks_catalog.uc_catalog.name}.${databricks_schema.bronze_schema.name}"

#   grant {
#     principal  = "users"
#     privileges = ["USAGE", "CREATE"]
#   }

#   grant {
#     principal  = data.databricks_current_user.me.alphanumeric
#     privileges = ["USAGE", "CREATE"]
#   }
# }

# resource "databricks_grants" "silver_schema_permissions" {
#   schema = "${databricks_catalog.uc_catalog.name}.${databricks_schema.silver_schema.name}"

#   grant {
#     principal  = "users"
#     privileges = ["USAGE", "CREATE"]
#   }

#   grant {
#     principal  = data.databricks_current_user.me.alphanumeric
#     privileges = ["USAGE", "CREATE"]
#   }
# }

# resource "databricks_grants" "gold_schema_permissions" {
#   schema = "${databricks_catalog.uc_catalog.name}.${databricks_schema.gold_schema.name}"

#   grant {
#     principal  = "users"
#     privileges = ["USAGE", "CREATE"]
#   }

#   grant {
#     principal  = data.databricks_current_user.me.alphanumeric
#     privileges = ["USAGE", "CREATE"]
#   }
# }

# resource "databricks_grants" "gold_scd2_schema_permissions" {
#   schema = "${databricks_catalog.uc_catalog.name}.${databricks_schema.gold_scd2_schema.name}"

#   grant {
#     principal  = "users"
#     privileges = ["USAGE", "CREATE"]
#   }

#   grant {
#     principal  = data.databricks_current_user.me.alphanumeric
#     privileges = ["USAGE", "CREATE"]
#   }
# }
