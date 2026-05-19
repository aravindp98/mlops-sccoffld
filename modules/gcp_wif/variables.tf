variable "gcp_project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "github_repository" {
  description = "GitHub repository allowed to authenticate, in owner/repo format."
  type        = string
}

variable "service_account_id" {
  description = "Service account ID used by GitHub Actions."
  type        = string
  default     = "github-actions-cicd"
}

variable "workload_identity_pool_id" {
  description = "Workload Identity Pool ID for GitHub Actions."
  type        = string
  default     = "github-actions-pool"
}

variable "workload_identity_provider_id" {
  description = "Workload Identity Provider ID for GitHub Actions."
  type        = string
  default     = "github-actions-provider"
}

variable "github_actions_project_roles" {
  description = "Project-level roles granted to the GitHub Actions service account."
  type        = list(string)
  default = [
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
  ]
}
