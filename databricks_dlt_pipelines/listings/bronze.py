import dlt
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Define the schema for the SQS messages
sqs_schema = StructType([
    StructField("event_type", StringType(), True),
    StructField("bucket_name", StringType(), True),
    StructField("object_key", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("file_content", StringType(), True)
])

# Read messages from SQS using Auto Loader
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
    .option("cloudFiles.queueUrl", 'https://sqs.eu-west-1.amazonaws.com/889562587392/raw-listing-bucket-events-queue')
    .option("cloudFiles.region", "eu-west-1")
    .option("cloudFiles.awsAccessKey", dbutils.secrets.get("aws-s3-access", "aws-access-key-id"))
    .option("cloudFiles.awsSecretKey", dbutils.secrets.get("aws-s3-access", "aws-secret-access-key"))
    .schema(sqs_schema)
    .load()
  )
