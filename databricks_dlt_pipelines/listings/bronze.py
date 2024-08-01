import dlt
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Define the schema for the SQS messages
schema = StructType([
    StructField("bucket_name", StringType(), True),
    StructField("object_key", StringType(), True),
    StructField("event_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("file_contents", StringType(), True)
])

# Read messages from the staging directory using Auto Loader
@dlt.table(
  name="listings_bronze",
  comment="Bronze table: Raw listings data containing S3 events relating to json objects for zoopla listings",
  table_properties={
    "quality": "bronze"
  }
)
def raw_listings_s3_events():
  return (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.region", "eu-west-1")
    .schema(schema)
    .load("s3a://zoopla-staging/listings/")
  )
