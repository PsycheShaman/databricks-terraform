# gold_scd2.py
from pyspark.sql import SparkSession

def run_merge():
    spark = SparkSession.builder.appName("MergeListings").getOrCreate()

    # Create the listings_scd_2 table if it doesn't already exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS houseful.zoopla_gold.listings_scd_2 (
      listing_id STRING,
      source STRING,
      parking STRING,
      outside_space STRING,
      price DOUBLE,
      transaction_type STRING,
      category STRING,
      latitude DOUBLE,
      longitude DOUBLE,
      postal_code STRING,
      street_name STRING,
      country_code STRING,
      town_or_city STRING,
      bathrooms INT,
      creation_date TIMESTAMP,
      total_bedrooms INT,
      display_address STRING,
      life_cycle_status STRING,
      summary_description STRING,
      start_date TIMESTAMP,
      end_date TIMESTAMP,
      is_current BOOLEAN
    )
    """
    
    spark.sql(create_table_query)

    merge_query = """
    MERGE INTO houseful.zoopla_gold.listings_scd_2 AS target
    USING (
      SELECT
        listing_id,
        source,
        parking,
        outside_space,
        price,
        transaction_type,
        category,
        latitude,
        longitude,
        postal_code,
        street_name,
        country_code,
        town_or_city,
        bathrooms,
        creation_date,
        total_bedrooms,
        display_address,
        life_cycle_status,
        summary_description,
        event_time AS start_date,
        NULL AS end_date,
        TRUE AS is_current,
        event_type
      FROM houseful.zoopla_silver.listings
    ) AS source
    ON target.listing_id = source.listing_id AND target.is_current = TRUE
    WHEN MATCHED AND source.event_type = 'delete' THEN
      UPDATE SET
        target.end_date = source.start_date,
        target.is_current = FALSE
    WHEN MATCHED AND (
        target.source <> source.source OR
        target.parking <> source.parking OR
        target.outside_space <> source.outside_space OR
        target.price <> source.price OR
        target.transaction_type <> source.transaction_type OR
        target.category <> source.category OR
        target.latitude <> source.latitude OR
        target.longitude <> source.longitude OR
        target.postal_code <> source.postal_code OR
        target.street_name <> source.street_name OR
        target.country_code <> source.country_code OR
        target.town_or_city <> source.town_or_city OR
        target.bathrooms <> source.bathrooms OR
        target.creation_date <> source.creation_date OR
        target.total_bedrooms <> source.total_bedrooms OR
        target.display_address <> source.display_address OR
        target.life_cycle_status <> source.life_cycle_status OR
        target.summary_description <> source.summary_description
    ) THEN
      UPDATE SET
        target.end_date = source.start_date,
        target.is_current = FALSE
    WHEN NOT MATCHED THEN
      INSERT (
        listing_id,
        source,
        parking,
        outside_space,
        price,
        transaction_type,
        category,
        latitude,
        longitude,
        postal_code,
        street_name,
        country_code,
        town_or_city,
        bathrooms,
        creation_date,
        total_bedrooms,
        display_address,
        life_cycle_status,
        summary_description,
        start_date,
        end_date,
        is_current
      )
      VALUES (
        source.listing_id,
        source.source,
        source.parking,
        source.outside_space,
        source.price,
        source.transaction_type,
        source.category,
        source.latitude,
        source.longitude,
        source.postal_code,
        source.street_name,
        source.country_code,
        source.town_or_city,
        source.bathrooms,
        source.creation_date,
        source.total_bedrooms,
        source.display_address,
        source.life_cycle_status,
        source.summary_description,
        source.start_date,
        source.end_date,
        source.is_current
      )
    """

    spark.sql(merge_query)
    spark.stop()

if __name__ == "__main__":
    run_merge()
