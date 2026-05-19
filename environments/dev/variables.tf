variable "github_repository" {
  description = "GitHub repository allowed to assume the OIDC role, in owner/repo format."
  type        = string
  default     = "aravindp98/mlops-sccoffld"
}

variable "gcp_project_id" {
  description = "Google Cloud project ID where Cloud Run and Artifact Registry will be created."
  type        = string
  default     = "devmlops-496015"

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

variable "cloud_run_bootstrap_image_uri" {
  description = "Public image used only to create the Cloud Run service before the first app image is pushed by CI."
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "cloud_run_allow_unauthenticated" {
  description = "Whether to allow public unauthenticated access to the Cloud Run service."
  type        = bool
  default     = true
}
