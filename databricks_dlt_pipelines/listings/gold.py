import dlt
from pyspark.sql.functions import col, row_number, last
from pyspark.sql.window import Window

@dlt.table(
  name="listings",
  comment="Gold table: Latest listings data for each listing currently on the website",
  table_properties={
    "quality": "gold"
  }
)
def listings_gold():
  silver_df = spark.table("houseful.zoopla_silver.listings")
  
  # Define the window specification
  window_spec = Window.partitionBy("listing_id").orderBy(col("event_time").desc())
  
  # Add a row number and event type for the latest record for each listing_id
  ranked_df = (
    silver_df
    .withColumn("row_number", row_number().over(window_spec))
  )
  
  # Filter to get only the latest records and exclude deleted ones
  latest_records_df = (
    ranked_df
    .filter(col("row_number") == 1)
    .filter(col("event_type") != "delete")
    .drop("row_number", "bucket_name", "object_key", "event_id", "event_type")
  )
  
  return latest_records_df
