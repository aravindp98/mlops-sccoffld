# Providers configuration
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

# --- GCP Resources ---

resource "google_project_service" "required_apis" {
  for_each = toset([
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
  ])

  project            = var.gcp_project_id
  service            = each.value
  disable_on_destroy = false
}

# Workload Identity Federation for GitHub Actions
module "gcp_wif" {
  source            = "../../modules/gcp_wif"
  gcp_project_id    = var.gcp_project_id
  github_repository = var.github_repository

  depends_on = [google_project_service.required_apis]
}

# Artifact Registry already exists, so do not recreate it here.
# module "artifact_registry" {
#   source        = "../../modules/artifact_registry"
#   project_id    = var.gcp_project_id
#   location      = var.gcp_region
#   repository_id = var.artifact_registry_repository_id
#   description   = "Docker images for the ML house prices service."
#
#   depends_on = [google_project_service.required_apis]
# }

# Cloud Run is paused until the image push path is working.
# module "cloud_run" {
#   source                = "../../modules/cloud_run"
#   project_id            = var.gcp_project_id
#   location              = var.gcp_region
#   service_name          = var.cloud_run_service_name
#   image_uri             = var.cloud_run_bootstrap_image_uri
#   allow_unauthenticated = var.cloud_run_allow_unauthenticated
#
#   depends_on = [module.artifact_registry]
# }
