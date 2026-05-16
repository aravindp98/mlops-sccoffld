variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "location" {
  description = "Google Cloud region for the Cloud Run service."
  type        = string
}

variable "service_name" {
  description = "Name of the Cloud Run service."
  type        = string
}

variable "image_uri" {
  description = "Full container image URI to deploy to Cloud Run."
  type        = string
}

variable "container_port" {
  description = "Port exposed by the container."
  type        = number
  default     = 8080
}

variable "cpu" {
  description = "CPU limit for the Cloud Run container."
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory limit for the Cloud Run container."
  type        = string
  default     = "512Mi"
}

variable "ingress" {
  description = "Ingress setting for the Cloud Run service."
  type        = string
  default     = "INGRESS_TRAFFIC_ALL"
}

variable "allow_unauthenticated" {
  description = "Whether to allow public unauthenticated access to the service."
  type        = bool
  default     = true
}
