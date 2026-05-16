output "service_url" {
  description = "Default URL of the App Runner service."
  value       = aws_apprunner_service.ml_service.service_url
}

output "service_arn" {
  description = "ARN of the App Runner service."
  value       = aws_apprunner_service.ml_service.arn
}

output "access_role_arn" {
  description = "ARN of the IAM role App Runner uses to pull from ECR."
  value       = aws_iam_role.apprunner_service_role.arn
}
