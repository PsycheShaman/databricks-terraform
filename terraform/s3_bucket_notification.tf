resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.z_raw.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.raw_listings_s3_event_lambda.arn
    events              = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]

    filter_suffix = ".json"
  }
}

resource "aws_lambda_permission" "allow_s3_to_invoke" {
  statement_id  = "AllowS3InvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.raw_listings_s3_event_lambda.function_name
  principal     = "s3.amazonaws.com"

  source_arn = aws_s3_bucket.z_raw.arn
}
