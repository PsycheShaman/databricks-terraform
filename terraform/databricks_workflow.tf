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
    spark_python_task {
      python_file = "/Workspace/Users/e642606c-2743-4a1c-8d38-55c714e2a315/houseful-technical-interview.git/databricks_dlt_pipelines/listings/gold_scd2.py"

    }

    new_cluster {
      num_workers   = 1
      spark_version = data.databricks_spark_version.latest.id
      node_type_id  = data.databricks_node_type.smallest.id
    }
  }
}
