import dlt
from pyspark.sql.functions import col, lit, current_timestamp
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

# Read messages from the staging directory using Auto Loader
@dlt.table(
  name="listings",
  comment="Silver table: Flattened listings data with SCD Type 2 functionality",
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
  
    # Implement SCD Type 2
    scd2_df = (
        flattened_df
        .withColumn("effective_date", col("event_time"))
        .withColumn("end_date", lit(None).cast(TimestampType()))
        .withColumn("is_current", lit(True))
    )
  
    # Merge with existing data in the silver table to handle updates and deletions
    merge_condition = "t.listing_id = s.listing_id AND t.end_date IS NULL"
  
    merge_query = """
        MERGE INTO houseful.zoopla_silver.listings t
        USING new_data s
        ON {merge_condition}
        WHEN MATCHED AND s.event_type = 'delete'
          THEN UPDATE SET t.end_date = s.event_time, t.is_current = False
        WHEN MATCHED AND s.event_type = 'create'
          THEN UPDATE SET t.end_date = s.event_time, t.is_current = False
        WHEN NOT MATCHED
          THEN INSERT (
            bucket_name, object_key, event_id, event_type, event_time, source, parking, outside_space, price, transaction_type, category, latitude, longitude,
            postal_code, street_name, country_code, town_or_city, bathrooms, listing_id, creation_date, total_bedrooms, display_address, life_cycle_status,
            summary_description, effective_date, end_date, is_current
          ) VALUES (
            s.bucket_name, s.object_key, s.event_id, s.event_type, s.event_time, s.source, s.parking, s.outside_space, s.price, s.transaction_type, s.category, s.latitude, s.longitude,
            s.postal_code, s.street_name, s.country_code, s.town_or_city, s.bathrooms, s.listing_id, s.creation_date, s.total_bedrooms, s.display_address, s.life_cycle_status,
            s.summary_description, s.effective_date, s.end_date, s.is_current
          )
    """.format(merge_condition=merge_condition)
  
    scd2_df.createOrReplaceTempView("new_data")
    spark.sql(merge_query)
  
    return spark.table("houseful.zoopla_silver.listings")
