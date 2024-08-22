resource "aws_s3_bucket" "sales_and_rentals_raw" {
  bucket = "sales_and_rentals-raw"
}

resource "aws_s3_bucket" "sales_and_rentals_staging" {
  bucket = "sales_and_rentals-staging"
}

resource "aws_s3_bucket_versioning" "sales_and_rentals_raw" {
  bucket = aws_s3_bucket.sales_and_rentals_raw.id
  versioning_configuration {
    status = "Enabled"
  }
}