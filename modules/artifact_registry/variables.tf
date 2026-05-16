variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "location" {
  description = "Google Cloud location for the Artifact Registry repository."
  type        = string
}

variable "repository_id" {
  description = "Artifact Registry repository ID."
  type        = string
}

variable "description" {
  description = "Description for the Artifact Registry repository."
  type        = string
  default     = "Docker image repository."
}
