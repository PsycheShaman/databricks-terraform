resource "aws_sfn_state_machine" "zoopla_processing_state_machine" {
  name     = "ZooplaProcessingStateMachine"
  role_arn = var.lambda_exec_role.arn
  definition = jsonencode({
    Comment: "Orchestrates Zoopla data processing",
    StartAt: "S3AndTableCountStart",
    States: {
      S3AndTableCountStart: {
        Type: "Task",
        Resource: "arn:aws:lambda:${aws_lambda_function.s3_and_table_count.arn}",
        Next: "InvokeZooplaPublisherService"
      },
      InvokeZooplaPublisherService: {
        Type: "Map",
        Iterator: {
          StartAt: "InvokeLambda",
          States: {
            InvokeLambda: {
              Type: "Task",
              Resource: "arn:aws:lambda:${aws_lambda_function.zoopla_publisher_service.arn}",
              End: true
            }
          }
        },
        ItemsPath: "$.iterations",
        MaxConcurrency: 10,
        Next: "WaitForCompletion"
      },
      WaitForCompletion: {
        Type: "Wait",
        Seconds: 60,
        Next: "TriggerDatabricksJob"
      },
      TriggerDatabricksJob: {
        Type: "Task",
        Resource: "arn:aws:states:::databricks:invokeJob",
        Parameters: {
          JobName: "Listings Pipeline Job",
          JobRunParameters: {}
        },
        Next: "S3AndTableCountEnd"
      },
      S3AndTableCountEnd: {
        Type: "Task",
        Resource: "arn:aws:lambda:${aws_lambda_function.s3_and_table_count.arn}",
        End: true
      }
    }
  })
}