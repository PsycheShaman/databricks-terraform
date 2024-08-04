import dlt
from pyspark.sql.functions import col, expr

@dlt.table(
  name="listings",
  comment="Silver table: Flattened listings data",
  table_properties={
    "quality": "silver"
  }
)
def listings_silver():
  bronze_df = spark.table("houseful.zoopla_bronze.listings")
  
  # Flatten the file_contents JSON structure
  flattened_df = bronze_df.select(
    col("bucket_name"),
    col("object_key"),
    col("event_id"),
    col("event_type"),
    col("event_time"),
    col("file_contents.source").alias("source"),
    col("file_contents.derived.parking")[0].alias("parking"),  # Extract the first element
    col("file_contents.derived.outside_space")[0].alias("outside_space"),  # Extract the first element
    col("file_contents.pricing.price").alias("price"),
    col("file_contents.pricing.transaction_type").alias("transaction_type"),
    col("file_contents.category").alias("category"),
    col("file_contents.location.coordinates.latitude").alias("latitude"),
    col("file_contents.location.coordinates.longitude").alias("longitude"),
    col("file_contents.location.postal_code").alias("postal_code"),
    col("file_contents.location.street_name").alias("street_name"),
    col("file_contents.location.country_code").alias("country_code"),
    col("file_contents.location.town_or_city").alias("town_or_city"),
    col("file_contents.bathrooms").alias("bathrooms"),
    col("file_contents.listing_id").alias("listing_id"),
    col("file_contents.creation_date").alias("creation_date"),
    col("file_contents.total_bedrooms").alias("total_bedrooms"),
    col("file_contents.display_address").alias("display_address"),
    col("file_contents.life_cycle_status").alias("life_cycle_status"),
    col("file_contents.summary_description").alias("summary_description")
  )

  # Infer listing_id from object_key if file is deleted
  inferred_df = (
    flattened_df
    .withColumn("listing_id", expr("CASE WHEN listing_id IS NULL THEN regexp_replace(split(object_key, '/')[1], '.json', '') ELSE listing_id END"))
  )

  return inferred_df

@dlt.table(
  name="listings_silver_stream",
  comment="Streaming silver table for listings data",
  table_properties={
    "quality": "silver"
  }
)
def listings_silver_stream():
    return (
        spark.table("houseful.zoopla_silver.listings")
        .select(
            col("bucket_name"),
            col("object_key"),
            col("event_id"),
            col("event_type"),
            col("event_time"),
            col("source"),
            col("parking"),
            col("outside_space"),
            col("price"),
            col("transaction_type"),
            col("category"),
            col("latitude"),
            col("longitude"),
            col("postal_code"),
            col("street_name"),
            col("country_code"),
            col("town_or_city"),
            col("bathrooms"),
            col("listing_id"),
            col("creation_date"),
            col("total_bedrooms"),
            col("display_address"),
            col("life_cycle_status"),
            col("summary_description")
        )
    )

dlt.create_streaming_table("listings_scd2")

dlt.apply_changes(
    target="listings_scd2",
    source="listings_silver_stream",
    keys=["listing_id"],
    sequence_by=col("event_time"),
    apply_as_deletes=expr("event_type = 'delete'"),
    except_column_list=["bucket_name", "object_key", "event_id", "event_type"],
    stored_as_scd_type="2"
)