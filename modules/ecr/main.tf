resource "aws_ecr_repository" "ml_model_repo" {
  name                 = var.repository_name
  image_tag_mutability = var.image_tag_mutability
}
