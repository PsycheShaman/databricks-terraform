resource "databricks_pipeline" "listings_bronze" {
  # Ingests events from SQS, containing details about `listing` JSON objects as they are created, deleted or updated on S3. These messages are created by a Lambda function triggered by S3 events.

  name        = "Listings Bronze"
  continuous  = false
  development = true
  catalog     = "houseful"
  target      = "zoopla_bronze"

  configuration = {
    "spark.master"                   = "local[*]"
    "spark.hadoop.fs.s3a.access.key" = "{{secrets/aws-s3-access/aws-access-key-id}}"
    "spark.hadoop.fs.s3a.secret.key" = "{{secrets/aws-s3-access/aws-secret-access-key}}"
  }

  cluster {
    label        = "default"
    num_workers  = 1
    node_type_id = "m5.large"
  }

  library {
    file {
      path = "${databricks_repo.houseful_technical_interview.path}/databricks_dlt_pipelines/listings/bronze.py"
    }
  }
}

resource "databricks_pipeline" "listings_silver" {

  name        = "Listings Silver"
  continuous  = false
  development = true
  catalog     = "houseful"
  target      = "zoopla_silver"

  configuration = {
    "spark.master"                   = "local[*]"
    "spark.hadoop.fs.s3a.access.key" = "{{secrets/aws-s3-access/aws-access-key-id}}"
    "spark.hadoop.fs.s3a.secret.key" = "{{secrets/aws-s3-access/aws-secret-access-key}}"
  }

  cluster {
    label        = "default"
    num_workers  = 1
    node_type_id = "m5.large"
  }

  library {
    file {
      path = "${databricks_repo.houseful_technical_interview.path}/databricks_dlt_pipelines/listings/silver.py"
    }
  }
}

resource "databricks_pipeline" "listings_gold" {

  name        = "Listings Gold"
  continuous  = false
  development = true
  catalog     = "houseful"
  target      = "zoopla_gold"

  configuration = {
    "spark.hadoop.fs.s3a.access.key" = "{{secrets/aws-s3-access/aws-access-key-id}}"
    "spark.hadoop.fs.s3a.secret.key" = "{{secrets/aws-s3-access/aws-secret-access-key}}"
    "spark.master"                   = "local[*]"
  }

  cluster {
    label        = "default"
    num_workers  = 1
    node_type_id = "m5.large"
  }

  library {
    file {
      path = "${databricks_repo.houseful_technical_interview.path}/databricks_dlt_pipelines/listings/gold.py"
    }
  }
}

# resource "databricks_pipeline" "listings_gold_scd_2" {

#   name        = "Listings Gold SCD 2"
#   continuous  = false
#   development = true
#   catalog     = "houseful"
#   target      = "zoopla_gold"

#   configuration = {
#     "spark.hadoop.fs.s3a.access.key" = "{{secrets/aws-s3-access/aws-access-key-id}}"
#     "spark.hadoop.fs.s3a.secret.key" = "{{secrets/aws-s3-access/aws-secret-access-key}}"
#     "spark.master"                   = "local[*]"
#   }

#   cluster {
#     label        = "default"
#     num_workers  = 1
#     node_type_id = "m5.large"
#   }

#   library {
#     file {
#       path = "${databricks_repo.houseful_technical_interview.path}/databricks_dlt_pipelines/listings/gold_scd2.py"
#     }
#   }
# }

# resource "databricks_pipeline" "original_end_to_end_listing_pipeline_deprecated" {
#   name        = "End-End Listing Pipeline (Deprecated)"
#   continuous  = false
#   development = true
#   catalog     = "houseful"
#   target      = "zoopla"

#   configuration = {
#     "spark.master"                   = "local[*]"
#     "spark.hadoop.fs.s3a.access.key" = "{{secrets/aws-s3-access/aws-access-key-id}}"
#     "spark.hadoop.fs.s3a.secret.key" = "{{secrets/aws-s3-access/aws-secret-access-key}}"
#   }

#   cluster {
#     label        = "default"
#     num_workers  = 1
#     node_type_id = "m5.large"
#   }

#   library {
#     file {
#       path = "${databricks_repo.houseful_technical_interview.path}/databricks_dlt_pipelines/dlt_process_listings.py"
#     }
#   }
# }

