# Service Cloud Resource Manager First
resource "google_project_service" "cloud_resource_manager" {
  project = var.id_project
  service = "cloudresourcemanager.googleapis.com"
}

