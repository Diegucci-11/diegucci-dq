resource "google_project_service" "enable_apis" {
  project = var.id_project
  # for_each = { for api in var.listado_apis_activar : api => api }
  for_each = toset(var.apis_list)
  service = each.key
}