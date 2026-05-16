output "service_id" {
  description = "ID of the Cloud Run service."
  value       = google_cloud_run_v2_service.service.id
}

output "service_url" {
  description = "URL of the Cloud Run service."
  value       = google_cloud_run_v2_service.service.uri
}
