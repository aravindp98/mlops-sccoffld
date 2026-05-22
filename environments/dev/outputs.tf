output "mlops_artifacts_bucket" {
  description = "GCS bucket name for DVC remote and MLflow artifacts."
  value       = module.mlops_artifacts_bucket.bucket_name
}

output "mlops_artifacts_bucket_url" {
  description = "gs:// URL for DVC remote config."
  value       = module.mlops_artifacts_bucket.bucket_url
}

output "artifact_registry_repository_url" {
  description = "Base URL of the Artifact Registry Docker repository."
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${var.artifact_registry_repository_id}"
}

output "artifact_registry_image_uri" {
  description = "Image URI used by CI/CD for the ML app image."
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${var.artifact_registry_repository_id}/${var.cloud_run_image_name}:${var.cloud_run_image_tag}"
}

output "gcp_workload_identity_provider" {
  description = "The full resource name of the Workload Identity Provider for GitHub Actions."
  value       = module.gcp_wif.workload_identity_provider_name
}

output "gcp_service_account" {
  description = "The email of the Service Account for GitHub Actions."
  value       = module.gcp_wif.service_account_email
}

output "cloud_run_service_url" {
  description = "URL of the Cloud Run service."
  value       = module.cloud_run.service_url
}

output "cloud_run_service_id" {
  description = "ID of the Cloud Run service."
  value       = module.cloud_run.service_id
}
