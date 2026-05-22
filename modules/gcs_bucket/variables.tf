variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "bucket_name" {
  description = "Globally unique GCS bucket name."
  type        = string
}

variable "location" {
  description = "GCS bucket location."
  type        = string
  default     = "US"
}

variable "force_destroy" {
  description = "Delete bucket even if it has objects."
  type        = bool
  default     = false
}

variable "versioning_enabled" {
  description = "Enable object versioning on the bucket."
  type        = bool
  default     = true
}

variable "writers" {
  description = "List of IAM members with objectAdmin access (e.g. serviceAccount:x@y.iam)."
  type        = list(string)
  default     = []
}
