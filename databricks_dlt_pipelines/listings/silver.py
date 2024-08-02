import dlt
from pyspark.sql.functions import col, expr, split, regexp_replace, explode
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DoubleType, ArrayType

# Define the schema for the file_contents field
file_contents_schema = StructType([
    StructField("source", StringType(), True),
    StructField("derived", StructType([
        StructField("parking", ArrayType(StringType()), True),
        StructField("outside_space", ArrayType(StringType()), True)
    ]), True),
    StructField("pricing", StructType([
        StructField("price", DoubleType(), True),
        StructField("transaction_type", StringType(), True)
    ]), True),
    StructField("category", StringType(), True),
    StructField("location", StructType([
        StructField("coordinates", StructType([
            StructField("latitude", DoubleType(), True),
            StructField("longitude", DoubleType(), True)
        ]), True),
        StructField("postal_code", StringType(), True),
        StructField("street_name", StringType(), True),
        StructField("country_code", StringType(), True),
        StructField("town_or_city", StringType(), True)
    ]), True),
    StructField("bathrooms", IntegerType(), True),
    StructField("listing_id", StringType(), True),
    StructField("creation_date", TimestampType(), True),
    StructField("total_bedrooms", IntegerType(), True),
    StructField("display_address", StringType(), True),
    StructField("life_cycle_status", StringType(), True),
    StructField("summary_description", StringType(), True)
])

# Define the schema for the SQS messages
schema = StructType([
    StructField("bucket_name", StringType(), True),
    StructField("object_key", StringType(), True),
    StructField("event_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("file_contents", file_contents_schema, True)
])

# Define the Silver table with flattened structure
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
    col("file_contents.derived.parking").alias("parking"),
    col("file_contents.derived.outside_space").alias("outside_space"),
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
  
  # Explode array columns to separate rows if needed
  exploded_df = (
    inferred_df
    .withColumn("parking", explode(expr("coalesce(parking, array(''))")))
    .withColumn("outside_space", explode(expr("coalesce(outside_space, array(''))")))
  )
  
  return exploded_df
