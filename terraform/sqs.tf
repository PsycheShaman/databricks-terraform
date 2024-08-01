resource "aws_sqs_queue" "listing_events_queue" {
  name                      = "raw-listing-bucket-events-queue"
  visibility_timeout_seconds = 30
  message_retention_seconds = 86400
}