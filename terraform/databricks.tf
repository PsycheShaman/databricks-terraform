resource "databricks_cluster" "dlt_cluster" {
  cluster_name            = "dlt-cluster"
  spark_version           = "7.3.x-scala2.12"
  node_type_id            = "i3.xlarge"
  autotermination_minutes = 20

  autoscale {
    min_workers = 1
    max_workers = 3
  }
}

resource "databricks_repo" "houseful_technical_interview" {
  url = var.git_url
}

resource "databricks_git_credential" "psycheshaman" {
  git_username          = var.git_username
  git_provider          = "gitHub"
  personal_access_token = var.git_personal_access_token
}

resource "databricks_pipeline" "listing_pipeline" {
  name           = "Listing Pipeline"
  storage        = "dbfs:/pipelines/listing-pipeline"
  configuration  = {
    "spark.master" = "local[*]"
  }

  library {
    file {
      path = "${databricks_repo.houseful_technical_interview.path}/dlt_process_listings.py"
    }
  }

  continuous = false  # Set to false to trigger the pipeline manually to save costs
}
