resource "aws_s3_bucket" "zoopla_raw" {
  bucket = "zoopla-raw"
}

resource "aws_s3_bucket" "zoopla_staging" {
  bucket = "zoopla-staging"
}

resource "aws_s3_bucket_versioning" "zoopla_raw" {
  bucket = aws_s3_bucket.zoopla_raw.id
  versioning_configuration {
    status = "Enabled"
  }
}