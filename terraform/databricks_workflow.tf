data "databricks_node_type" "smallest" {
  local_disk = true
}

data "databricks_spark_version" "latest" {
  latest = true
}

resource "databricks_job" "listings_pipeline_job" {
  name        = "Listings Pipeline Job"
  description = "This job orchestrates the Bronze, Silver, and Gold DLT pipelines for the listings data."

  # Task for the Bronze pipeline
  task {
    task_key = "bronze_task"
    pipeline_task {
      pipeline_id = databricks_pipeline.listings_bronze.id
    }
  }

  # Task for the Silver pipeline
  task {
    task_key = "silver_task"
    depends_on {
      task_key = "bronze_task"
    }
    pipeline_task {
      pipeline_id = databricks_pipeline.listings_silver.id
    }
  }

  # Task for the Gold pipeline
  task {
    task_key = "gold_task"
    depends_on {
      task_key = "silver_task"
    }
    pipeline_task {
      pipeline_id = databricks_pipeline.listings_gold.id
    }
  }

  task {
    task_key = "gold_scd2_task"
    depends_on {
      task_key = "gold_task"
    }
    pipeline_task {
      pipeline_id = databricks_pipeline.listings_gold_scd_2.id
    }
  }
}