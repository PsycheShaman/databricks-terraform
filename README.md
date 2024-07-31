# houseful-technical-interview

## Publishing Service

The purpose of this Lambda function is to simulate the backend publishing service of the Zoopla web application. This function generates JSON objects representing property listings with realistic values. These listings are stored in an S3 bucket and can be created, updated, or deleted based on certain probabilities.

### Features
- Generates realistic property listings with attributes such as address, pricing, parking, and outside space.
- Randomly updates or deletes existing listings.
- Stores listings in an S3 bucket named `z-raw`.

## Terraform

