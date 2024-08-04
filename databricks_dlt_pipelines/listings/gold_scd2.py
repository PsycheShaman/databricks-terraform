import dlt
from pyspark.sql.functions import col

# Define the SCD Type 2 table using apply_changes
@dlt.table(
  name="listings_scd2",
  comment="Gold table: Listings SCD Type 2 to view historical changes",
  table_properties={
    "quality": "gold"
  }
)
@dlt.expect_or_drop("valid_event_type", col("event_type").isin("create", "update", "delete"))
def listings_scd2():
  return dlt.apply_changes(
    target = "listings_scd2",
    source = "houseful.zoopla_silver.listings",
    keys = ["listing_id"],
    sequence_by = col("event_time"),
    apply_as_deletes = col("event_type") == "delete",
    except_column_list = ["row_number", "bucket_name", "object_key", "event_id", "event_type"],
    stored_as_scd_type = "2",
    query_name = "listings_scd2_apply_changes"
  )

