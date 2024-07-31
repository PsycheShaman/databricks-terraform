import dlt
from pyspark.sql.functions import col

# Define the schema for the JSON files
schema = """
  source STRING,
  derived STRUCT<
    parking: ARRAY<STRING>,
    outside_space: ARRAY<STRING>
  >,
  pricing STRUCT<
    price: DOUBLE,
    transaction_type: STRING
  >,
  category STRING,
  location STRUCT<
    coordinates: STRUCT<
      latitude: DOUBLE,
      longitude: DOUBLE
    >,
    postal_code: STRING,
    street_name: STRING,
    country_code: STRING,
    town_or_city: STRING
  >,
  bathrooms INTEGER,
  listing_id INTEGER,
  creation_date TIMESTAMP,
  total_bedrooms INTEGER,
  display_address STRING,
  life_cycle_status STRING,
  summary_description STRING
"""

# Ingest JSON data from S3
@dlt.table(
  comment="Raw listings data"
)
def raw_listings():
  return (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .schema(schema)
    .load("s3a://z-raw/listings/")
  )

# Flatten the nested fields and create a table suitable for querying
@dlt.table(
  comment="Flattened listings data"
)
def flattened_listings():
  return (
    dlt.read("raw_listings")
    .select(
      col("source"),
      col("derived.parking").alias("parking"),
      col("derived.outside_space").alias("outside_space"),
      col("pricing.price"),
      col("pricing.transaction_type"),
      col("category"),
      col("location.coordinates.latitude"),
      col("location.coordinates.longitude"),
      col("location.postal_code"),
      col("location.street_name"),
      col("location.country_code"),
      col("location.town_or_city"),
      col("bathrooms"),
      col("listing_id"),
      col("creation_date"),
      col("total_bedrooms"),
      col("display_address"),
      col("life_cycle_status"),
      col("summary_description")
    )
  )
