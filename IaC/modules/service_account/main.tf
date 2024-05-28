provider "google" {
  project     = var.id_project
  region      = var.region_project
}

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

resource "google_project_iam_member" "bigquery_admin_role" {
  project = var.id_project
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.data_quality_service_account.email}"
}

resource "google_project_iam_member" "composer_worker_role" {
  project = var.id_project
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.data_quality_service_account.email}"
}

resource "google_project_iam_member" "composer_extv2_role" {
  project = var.id_project
  role    = "roles/composer.ServiceAgentV2Ext"
  member  = "serviceAccount: service-${project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}
