terraform {
  backend "s3" {
    bucket = "z--tf"
    key    = "terraform/state"
    region = "eu-west-1"
  }
}