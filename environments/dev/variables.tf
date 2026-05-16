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

variable "gcp_project_id" {
  description = "Google Cloud project ID where Cloud Run and Artifact Registry will be created."
  type        = string

  validation {
    condition     = length(trimspace(var.gcp_project_id)) > 0
    error_message = "gcp_project_id must be set to a non-empty Google Cloud project ID."
  }
}

variable "gcp_region" {
  description = "Google Cloud region for Cloud Run and Artifact Registry."
  type        = string
  default     = "us-central1"
}

variable "artifact_registry_repository_id" {
  description = "Artifact Registry repository ID for Docker images."
  type        = string
  default     = "mlops-house-prices"
}

variable "cloud_run_service_name" {
  description = "Name of the Cloud Run service."
  type        = string
  default     = "mlops-house-prices-service"
}

variable "cloud_run_image_name" {
  description = "Docker image name in Artifact Registry."
  type        = string
  default     = "mlops-app"
}

variable "cloud_run_image_tag" {
  description = "Docker image tag for Cloud Run to deploy."
  type        = string
  default     = "latest"
}

variable "cloud_run_allow_unauthenticated" {
  description = "Whether to allow public unauthenticated access to the Cloud Run service."
  type        = bool
  default     = true
}
