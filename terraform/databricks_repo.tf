
resource "databricks_repo" "databricks_terraform" {
  url = var.git_url
}

resource "databricks_git_credential" "psycheshaman" {
  git_username          = var.git_username
  git_provider          = "gitHub"
  personal_access_token = var.git_personal_access_token
}