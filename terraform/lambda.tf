# lambda.tf

resource "aws_lambda_function" "zoopla_publisher_service" {
  filename         = "function.zip"
  function_name    = "zoopla_publisher_service"
  role             = var.lambda_exec_role_id
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("function.zip")
  runtime          = "python3.10"
  timeout          = 60

  environment {
    variables = {
      BUCKET_NAME = var.s3_bucket
    }
  }
}
