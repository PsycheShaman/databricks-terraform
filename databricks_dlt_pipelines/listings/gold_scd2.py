import dlt
from pyspark.sql.functions import col, current_timestamp, lit, lead, when
from pyspark.sql.window import Window

@dlt.table(
  name="listings_scd2",
  comment="Gold table: Listings SCD Type 2 to view historical changes",
  table_properties={
    "quality": "gold"
  }
)
def listings_scd2():
  # Read from the silver table
  silver_df = dlt.read_stream("listings_silver")

  # Define the window specification for detecting changes
  window_spec = Window.partitionBy("listing_id").orderBy("event_time")

  # Determine the start and end dates for each record
  scd2_df = (
    silver_df
    .withColumn("start_date", col("event_time"))
    .withColumn("end_date", lead(col("event_time"), 1).over(window_spec))
    .withColumn("is_current", when(lead(col("event_time"), 1).over(window_spec).isNull(), True).otherwise(False))
  )

  # Identify deleted records
  delete_df = silver_df.filter(col("event_type") == "delete").select("listing_id", "event_time")

  # Update the is_current and end_date for deleted records
  scd2_df = (
    scd2_df
    .join(delete_df, "listing_id", "left")
    .withColumn("is_current", when(col("delete_df.event_time").isNotNull(), False).otherwise(col("is_current")))
    .withColumn("end_date", when(col("delete_df.event_time").isNotNull(), col("delete_df.event_time")).otherwise(col("end_date")))
  )

  return scd2_df

@dlt.table(
  name="current_listings",
  comment="Gold table: Current active listings"
)
@dlt.expect_or_drop("valid_is_current", col("is_current") == True)
def current_listings():
  return dlt.read("listings_scd2").filter(col("is_current") == True)
