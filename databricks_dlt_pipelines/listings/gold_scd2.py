import dlt
from pyspark.sql.functions import col

@dlt.view
def listings_silver():
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
    target = "listings_scd2",
    source = "listings_silver",
    keys = ["listing_id"],
    sequence_by = col("event_time"),
    apply_as_deletes = col("event_type") == "delete",
    except_column_list = ["bucket_name", "object_key", "event_id", "event_type"],
    stored_as_scd_type = "2"
)
