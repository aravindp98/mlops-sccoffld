output "ecr_repository_url" {
  description = "URL of the ECR repository."
  value       = module.ecr.repository_url
}

output "role_arn" {
  description = "ARN of the GitHub Actions IAM role."
  value       = module.iam_github.role_arn
}
