# Service Cloud Resource Manager First
resource "google_project_service" "cloud_resource_manager" {
  project = var.project_id
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "enable_apis" {
  project = var.id_project
  for_each = toset(var.apis_list)
  service = each.key
  depends_on = [google_project_service.cloud_resource_manager]
}