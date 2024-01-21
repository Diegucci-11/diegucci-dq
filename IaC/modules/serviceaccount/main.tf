resource "google_service_account" "data_quality_service_account" {
  account_id   = var.service_account
  display_name = "DQ service account"
}

resource "google_project_iam_member" "editor_role" {
  project = var.id_project
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.data_quality_service_account.email}"
}

resource "google_project_iam_member" "token_creator_role" {
  project = var.id_project
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:${google_service_account.data_quality_service_account.email}"
}

resource "google_project_iam_member" "secret_accessor_role" {
  project = var.id_project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.data_quality_service_account.email}"
}

resource "google_service_account_key" "my_service_account_key" {
  service_account_id = google_service_account.data_quality_service_account.name
}

resource "google_secret_manager_secret" "my_service_account_secret" {
  secret_id = var.name_secret
}

resource "google_secret_manager_secret_version" "my_service_account_secret_version" {
  secret = google_secret_manager_secret.my_service_account_secret.id
  secret_data = google_service_account_key.my_service_account_key.private_key
} 