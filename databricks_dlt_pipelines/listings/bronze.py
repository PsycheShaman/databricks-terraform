import dlt
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, ArrayType

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

# Define the schema for the S3 event messages
schema = StructType([
    StructField("bucket_name", StringType(), True),
    StructField("object_key", StringType(), True),
    StructField("event_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("file_contents", file_contents_schema, True)
])

# Read messages from the staging directory using Auto Loader
@dlt.table(
  name="listings",
  comment="Bronze table: Raw listings data containing S3 events relating to json objects for sales_and_rentals listings",
  table_properties={
    "quality": "bronze"
  }
)
def raw_listings_s3_events():
  return (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.useNotifications", "true")  # Ensure this is set to use notifications
    .option("cloudFiles.region", "eu-west-1")
    .option("cloudFiles.awsAccessKey", dbutils.secrets.get("aws-s3-access", "aws-access-key-id"))
    .option("cloudFiles.awsSecretKey", dbutils.secrets.get("aws-s3-access", "aws-secret-access-key"))
    .schema(schema)
    .load("s3a://sales_and_rentals-staging/listings/")
  )
