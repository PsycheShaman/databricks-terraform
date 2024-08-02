import dlt
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

# Define the Gold table with the latest records for each listing
@dlt.table(
  name="listings_gold",
  comment="Gold table: Latest listings data for each listing currently on the website",
  table_properties={
    "quality": "gold"
  }
)
def listings_gold():
  silver_df = dlt.read("listings_silver")
  
  # Define the window specification
  window_spec = Window.partitionBy("listing_id").orderBy(col("event_time").desc())
  
  # Filter out the latest records and exclude deleted records
  latest_records_df = (
    silver_df
    .withColumn("row_number", row_number().over(window_spec))
    .filter((col("row_number") == 1) & (col("event_type") != "delete"))
    .drop("row_number", "bucket_name", "object_key", "event_id", "event_type", "event_time")
  )
  
  return latest_records_df
