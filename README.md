# Databricks Terraform

The goal of this repo is to show off some of my skills in Databricks and Terraform, I hope you enjoy it ;) 

In order to do this, I designed a CI/CD pipeline and a data ingestion/processing pipeline that takes real estate listing data simulated by a Lambda funtion into S3, ingests it into Databricks via Autoloader and transforms it through a medallion architecture of Delta Live Tables in order to expose it as a Databricks Dashboard.

## Scenario Overview

Real Estate Inc. has a backend service, which emits JSON messages to an S3 bucket, whenever a listing on their website is created, updated, or deleted. This data needs to be flattened and consumed via a dashboard, containing only the currently active listings on the website.

## Solution Overview

The solution consists of two main parts:

1. **Lambda Functions**: For handling the publishing service and the ingestion of listing CRUD events.
2. **Data Pipeline**: Using Delta Live Tables (DLT) to process and manage the data, implementing both Bronze, Silver, and Gold tables, including an SCD2 table for historical changes.
3. **CI/CD Pipeline**: Utilizing GitHub Actions for continuous integration and deployment.
4. **Infrastructure as Code**: Managing infrastructure with Terraform.

---

## Lambda Functions

### sales_and_rentals Publishing Service (`sales_and_rentals_publishing_service`)

This Lambda function simulates the behavior of the publishing service by generating and updating listings. It handles:

- **Creation of Listings**: Generates new listings with random data.
- **Updating Listings**: Updates existing listings with random modifications.
- **Deletion of Listings**: Deletes existing listings based on a random choice.

### Raw Listings S3 Event Lambda (`raw_listings_s3_event_lambda`)

This Lambda function captures the CRUD events from the publishing service and reflects them onto a staging bucket. It handles:

- **Detection of Events**: Listens for object creation and deletion events in the S3 bucket.
- **Processing Events**: Retrieves the file contents for created objects and constructs a message payload.
- **Storing Events**: Writes the processed events to a staging S3 bucket with a unique hash identifier.

---

## Data Pipeline

### Bronze Table

- **Raw Listings Data**: Contains raw listings data with S3 events, capturing JSON objects from the sales_and_rentals listings.

### Silver Table

- **Flattened Listings Data**: Processes the raw data to flatten the JSON structure, removing nested fields and ensuring each column represents a property from the original JSON document.

### Gold Table

- **Current Listings Data**: Maintains the latest state of each listing, including deletions, and ensures the data is available for querying from a Data Warehouse.

### Gold SCD2 Table

- **Historical Listings Data**: Tracks the SCD Type 2 history for listings, including records that have been deleted, with start and end timestamps for validity and an `is_current` boolean to indicate the current record.

---

## Infrastructure as Code (IaC)

### Terraform

The infrastructure is managed in its entirety by Terraform.

---

## CI/CD Pipeline

### GitHub Actions

GitHub Actions is used for continuous integration and deployment. The workflow automates the following steps:

1. **Zipping Lambda Functions**: Packages the Lambda functions.
2. **Terraform Initialization**: Initializes Terraform in the workspace.
3. **Terraform Plan and Apply**: Applies the Terraform plan to deploy the infrastructure.

The CI/CD pipeline ensures that any changes to the codebase or infrastructure are automatically tested and deployed, maintaining consistency and reliability in the deployment process.
