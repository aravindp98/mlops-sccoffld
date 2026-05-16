variable "service_name" {
  description = "Name of the AWS App Runner service."
  type        = string
  default     = "mlops-house-prices-service"
}

variable "image_uri" {
  description = "Full ECR image URI for App Runner to deploy, including tag."
  type        = string
}
