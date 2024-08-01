resource "aws_s3_bucket" "z_raw" {
  bucket = "z-raw"
}

resource "aws_s3_bucket" "z_staging" {
  bucket = "z-staging"
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.z_raw.id
  versioning_configuration {
    status = "Enabled"
  }
}