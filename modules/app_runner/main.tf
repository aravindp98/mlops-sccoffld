# 1. IAM Role so App Runner can pull from ECR
resource "aws_iam_role" "apprunner_service_role" {
  name = "AppRunnerECRAccessRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "build.apprunner.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_policy" {
  role       = aws_iam_role.apprunner_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# 2. The App Runner Service itself
resource "aws_apprunner_service" "ml_service" {
  service_name = var.service_name

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_service_role.arn
    }
    image_repository {
      image_identifier      = var.image_uri
      image_repository_type = "ECR"
      image_configuration {
        port = "8080" # Matches your Flask app
      }
    }
    auto_deployments_enabled = true # The "Continuous" in CD
  }

  instance_configuration {
    cpu    = "1024" # 1 vCPU
    memory = "2048" # 2 GB RAM
  }
}