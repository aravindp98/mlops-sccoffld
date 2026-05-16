output "ecr_repository_url" {
  description = "URL of the ECR repository."
  value       = module.ecr.repository_url
}

output "role_arn" {
  description = "ARN of the GitHub Actions IAM role."
  value       = module.iam_github.role_arn
}

output "artifact_registry_repository_url" {
  description = "Base URL of the Artifact Registry Docker repository."
  value       = module.artifact_registry.repository_url
}

output "cloud_run_service_url" {
  description = "URL of the Cloud Run service."
  value       = module.cloud_run.service_url
}

output "cloud_run_service_id" {
  description = "ID of the Cloud Run service."
  value       = module.cloud_run.service_id
}
