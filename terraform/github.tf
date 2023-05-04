resource "github_repository" "main" {
  name        = "prfiesta"
  description = "Analyze Individual Contributor Pull Requests"
  visibility  = "private"

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

# OUTPUTS

output "github_repository_ssh_clone_url" {
  value = github_repository.main.ssh_clone_url
}
