resource "aws_lambda_function" "zoopla_publisher_service" {
  filename         = "zoopla_publishing_service.zip"
  function_name    = "zoopla_publisher_service"
  role             = var.lambda_exec_role_id
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("zoopla_publishing_service.zip")
  runtime          = "python3.10"
  timeout          = 60

  environment {
    variables = {
      BUCKET_NAME = var.s3_bucket
    }
  }
}

resource "aws_lambda_function" "raw_listings_s3_event_lambda" {
  filename         = "raw_listings_s3_event_lambda.zip"
  function_name    = "raw_listings_s3_event_lambda"
  role             = var.lambda_exec_role_id
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = filebase64sha256("raw_listings_s3_event_lambda.zip")

  environment {
    variables = {
      BUCKET_NAME = var.s3_bucket
    }
  }
}

resource "aws_lambda_function" "s3_and_table_count" {
  filename         = "s3_and_table_count.zip"
  function_name    = "s3_and_table_count"
  role             = var.lambda_exec_role_id
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("s3_and_table_count.zip")
  runtime          = "python3.10"
  timeout          = 60

  environment {
    variables = {
      DATABRICKS_HOST = var.databricks_host
      DATABRICKS_TOKEN = var.databricks_token
    }
  }
}
