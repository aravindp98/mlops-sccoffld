output "repository_url" {
  description = "URL of the ECR repository."
  value       = aws_ecr_repository.ml_model_repo.repository_url
}
