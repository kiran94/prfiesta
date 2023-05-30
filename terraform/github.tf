resource "github_repository" "main" {
  name         = "prfiesta"
  description  = "Collect and Analyze Individual Contributor Pull Requests"
  visibility   = "public"
  homepage_url = "https://pypi.org/project/prfiesta/"

  has_projects  = false
  has_wiki      = false
  has_downloads = false

  allow_merge_commit     = false
  allow_rebase_merge     = false
  allow_auto_merge       = false
  allow_squash_merge     = true
  delete_branch_on_merge = true

  topics = [
    "pull-request",
    "pull-request-review",
    "performance-review"
  ]
}

resource "github_branch_protection" "main" {
  repository_id       = github_repository.main.node_id
  pattern             = "main"
  enforce_admins      = false
  allows_deletions    = false
  allows_force_pushes = false
}

# SECRETS

resource "github_actions_secret" "pypi_token" {
  repository      = github_repository.main.name
  secret_name     = "POETRY_PYPI_TOKEN_PYPI"
  plaintext_value = data.aws_ssm_parameter.pypi_token.value
}

# OUTPUTS

output "github_repository_ssh_clone_url" {
  value = github_repository.main.ssh_clone_url
}
