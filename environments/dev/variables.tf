variable "aws_region" {
  description = "AWS region where resources will be created."
  type        = string
  default     = "us-east-1"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository for the ML model image."
  type        = string
  default     = "mlops-house-prices"
}

variable "ecr_image_tag_mutability" {
  description = "Image tag mutability setting for the ECR repository."
  type        = string
  default     = "MUTABLE"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the OIDC role, in owner/repo format."
  type        = string
  default     = "aravindp98/mlops-sccoffld"
}

variable "github_actions_role_name" {
  description = "Name of the IAM role assumed by GitHub Actions."
  type        = string
  default     = "GitHubActionRole"
}
