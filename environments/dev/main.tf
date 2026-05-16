terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_project_service" "cloud_run" {
  project            = var.gcp_project_id
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry" {
  project            = var.gcp_project_id
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

module "ecr" {
  source = "../../modules/ecr"

  repository_name      = var.ecr_repository_name
  image_tag_mutability = var.ecr_image_tag_mutability
}

module "iam_github" {
  source = "../../modules/iam_github"

  github_repository = var.github_repository
  role_name         = var.github_actions_role_name
}

module "artifact_registry" {
  source = "../../modules/artifact_registry"

  project_id    = var.gcp_project_id
  location      = var.gcp_region
  repository_id = var.artifact_registry_repository_id
  description   = "Docker images for the ML house prices service."

  depends_on = [google_project_service.artifact_registry]
}

module "cloud_run" {
  source = "../../modules/cloud_run"

  project_id            = var.gcp_project_id
  location              = var.gcp_region
  service_name          = var.cloud_run_service_name
  image_uri             = "${module.artifact_registry.repository_url}/${var.cloud_run_image_name}:${var.cloud_run_image_tag}"
  container_port        = 8080
  allow_unauthenticated = var.cloud_run_allow_unauthenticated

  depends_on = [google_project_service.cloud_run]
}
