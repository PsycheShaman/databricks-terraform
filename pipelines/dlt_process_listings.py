import dlt
import dbutils
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

# Ingest JSON data from S3 using Autoloader
@dlt.table(
  comment="Raw listings data"
)
def raw_listings():
  return (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.useNotifications", "true")
    .option("cloudFiles.includeExistingFiles", "true")
    .option("cloudFiles.region", "eu-west-1")  # Specify your AWS region
    .option("cloudFiles.access.key", dbutils.secrets.get("aws-s3-access", "aws-access-key-id"))
    .option("cloudFiles.secret.key", dbutils.secrets.get("aws-s3-access", "aws-secret-access-key"))
    .schema(schema)
    .load("s3a://z-raw/listings/")
  )
