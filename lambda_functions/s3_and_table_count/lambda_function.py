import json
import boto3
import databricks.sql as dbsql

s3 = boto3.client('s3')
DATABRICKS_HOST = 'your-databricks-host'
DATABRICKS_TOKEN = 'your-databricks-token'

def lambda_handler(event, context):
    # List files in zoopla-raw and zoopla-staging
    zoopla_raw_files = s3.list_objects_v2(Bucket='zoopla-raw')['KeyCount']
    zoopla_staging_files = s3.list_objects_v2(Bucket='zoopla-staging')['KeyCount']

    # Count records in Delta Live Tables
    connection = dbsql.connect(
        server_hostname=DATABRICKS_HOST,
        access_token=DATABRICKS_TOKEN
    )

    cursor = connection.cursor()
    tables = ["houseful.zoopla_bronze.listings", "houseful.zoopla_silver.listings", "houseful.zoopla_gold.listings"]
    counts = {}
    for table in tables:
        cursor.execute(f"SELECT COUNT(1) FROM {table}")
        counts[table] = cursor.fetchone()[0]

    # Log results
    print(f"zoopla-raw file count: {zoopla_raw_files}")
    print(f"zoopla-staging file count: {zoopla_staging_files}")
    for table, count in counts.items():
        print(f"{table} record count: {count}")

    cursor.close()
    connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'zoopla_raw_files': zoopla_raw_files,
            'zoopla_staging_files': zoopla_staging_files,
            'table_counts': counts
        })
    }
