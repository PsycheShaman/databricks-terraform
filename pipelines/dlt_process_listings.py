import dlt
from pyspark.sql.functions import col, current_date, first

# Define the schema for the JSON files
schema = """
  source: STRING,
  derived: STRUCT<
    parking: ARRAY<STRING>,
    outside_space: ARRAY<STRING>
  >,
  pricing: STRUCT<
    price: DOUBLE,
    transaction_type: STRING
  >,
  category: STRING,
  location: STRUCT<
    coordinates: STRUCT<
      latitude: DOUBLE,
      longitude: DOUBLE
    >,
    postal_code: STRING,
    street_name: STRING,
    country_code: STRING,
    town_or_city: STRING
  >,
  bathrooms: INTEGER,
  listing_id: INTEGER,
  creation_date: TIMESTAMP,
  total_bedrooms: INTEGER,
  display_address: STRING,
  life_cycle_status: STRING,
  summary_description: STRING
"""


# Ingest JSON data from S3 using Auto Loader
@dlt.table(
  comment="Bronze table: Raw listings data"
)
def raw_listings():
  return (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.useNotifications", "true")
    .option("cloudFiles.includeExistingFiles", "true")
    .option("cloudFiles.region", "eu-west-1")
    .option("cloudFiles.access.key", dbutils.secrets.get("aws-s3-access", "aws-access-key-id"))
    .option("cloudFiles.secret.key", dbutils.secrets.get("aws-s3-access", "aws-secret-access-key"))
    .schema(schema)
    .load("s3a://z-raw/listings/")
  )

# Flatten the JSON structure and add a date column
@dlt.table(
  comment="Silver table: Flattened listings data",
  table_properties={
    "quality": "silver"
  }
)
def flattened_listings():
  return (
    dlt.read("raw_listings")
    .select(
      "source",
      "derived.parking",
      "derived.outside_space",
      "pricing.price",
      "pricing.transaction_type",
      "category",
      col("location.coordinates.latitude").alias("latitude"),
      col("location.coordinates.longitude").alias("longitude"),
      "location.postal_code",
      "location.street_name",
      "location.country_code",
      "location.town_or_city",
      "bathrooms",
      "listing_id",
      "creation_date",
      "total_bedrooms",
      "display_address",
      "life_cycle_status",
      "summary_description",
      current_date().alias("processing_date")
    )
  )

# Create a daily snapshot table
@dlt.table(
  comment="Gold table: Daily snapshot of listings",
  table_properties={
    "quality": "gold"
  }
)
def daily_snapshot():
  return (
    dlt.read("flattened_listings")
    .groupBy(
      "listing_id",
      "processing_date"
    )
    .agg(
      first("source").alias("source"),
      first("parking").alias("parking"),
      first("outside_space").alias("outside_space"),
      first("price").alias("price"),
      first("transaction_type").alias("transaction_type"),
      first("category").alias("category"),
      first("latitude").alias("latitude"),
      first("longitude").alias("longitude"),
      first("postal_code").alias("postal_code"),
      first("street_name").alias("street_name"),
      first("country_code").alias("country_code"),
      first("town_or_city").alias("town_or_city"),
      first("bathrooms").alias("bathrooms"),
      first("creation_date").alias("creation_date"),
      first("total_bedrooms").alias("total_bedrooms"),
      first("display_address").alias("display_address"),
      first("life_cycle_status").alias("life_cycle_status"),
      first("summary_description").alias("summary_description")
    )
  )
