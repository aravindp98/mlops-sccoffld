variable "github_repository" {
  description = "GitHub repository allowed to assume the OIDC role, in owner/repo format."
  type        = string
}

variable "role_name" {
  description = "Name of the IAM role assumed by GitHub Actions."
  type        = string
  default     = "GitHubActionRole"
}

variable "github_oidc_thumbprint" {
  description = "Thumbprint for GitHub Actions OIDC provider."
  type        = string
  default     = "6938fd4d98bab03faadb97b34396831e3780aea1"
}
