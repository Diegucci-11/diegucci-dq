resource "google_project_service" "enable_apis" {
  project = var.id_project
  for_each = toset(var.apis_list)
  service = each.key
}

