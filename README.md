# Houseful Technical Interview Submission

This repository contains the solution for the scenario-based question provided during the Houseful technical interview. The goal is to design a CI/CD pipeline and a data ingestion/processing pipeline that takes the data from source to target for the Zoopla web application's backend service.

## Scenario Overview

We have a backend service, the "publishing service," that handles listings from estate agents and emits JSON messages stored in an S3 bucket. These messages are emitted when a listing is created, updated, or deleted.

## Requirements

1. **One row per listing, per day the listing is live on the site**
2. **One column per each property in the JSON document**
3. **No nested fields**
4. **Table available for query from a Data Warehouse**

## Solution Overview

The solution consists of two main parts:

1. **Lambda Functions**: For handling the publishing service and the ingestion of listing CRUD events.
2. **Data Pipeline**: Using Delta Live Tables (DLT) to process and manage the data, implementing both Bronze, Silver, and Gold tables, including an SCD2 table for historical changes.

---

## Lambda Functions

### Zoopla Publishing Service (`zoopla_publishing_service`)

This Lambda function simulates the behavior of the publishing service by generating and updating listings. It handles:

- **Creation of Listings**: Generates new listings with random data.
- **Updating Listings**: Updates existing listings with random modifications.
- **Deletion of Listings**: Deletes existing listings based on a random choice.

### Raw Listings S3 Event Lambda (`raw_listings_s3_event_lambda`)

This Lambda function captures the CRUD events from the publishing service and reflects them onto a staging bucket. It handles:

- **Detection of Events**: Listens for object creation and deletion events in the S3 bucket.
- **Processing Events**: Retrieves the file contents for created objects and constructs a message payload.
- **Storing Events**: Writes the processed events to a staging S3 bucket with a unique hash identifier.

## Data Pipeline

### Bronze Table

- **Raw Listings Data**: Contains raw listings data with S3 events, capturing JSON objects from the Zoopla listings.

### Silver Table

- **Flattened Listings Data**: Processes the raw data to flatten the JSON structure, removing nested fields and ensuring each column represents a property from the original JSON document.

### Gold Table

- **Current Listings Data**: Maintains the latest state of each listing, including deletions, and ensures the data is available for querying from a Data Warehouse.

### Gold SCD2 Table

- **Historical Listings Data**: Tracks the SCD Type 2 history for listings, including records that have been deleted, with start and end timestamps for validity and an `is_current` boolean to indicate the current record.
