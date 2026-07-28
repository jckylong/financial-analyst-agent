output "cloud_run_url" {
  description = "URL of the deployed Cloud Run agent service"
  value       = google_cloud_run_v2_service.agent_service.uri
}

output "artifact_repository" {
  description = "Artifact Registry Docker Repository path"
  value       = google_artifact_registry_repository.agent_repo.name
}
