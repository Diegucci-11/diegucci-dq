provider "google" {
  alias = "impersonation"

  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}

provider "google" {
  access_token = data.google_service_account_access_token.terraform_admin.access_token

  scopes = [
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email"
  ]
}

provider "google-beta" {
  region  = var.zone
  project = var.project_id

  access_token = data.google_service_account_access_token.terraform_admin.access_token

  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email"
  ]
}

data "google_service_account_access_token" "terraform_admin" {
  target_service_account = local.service_accounts.terraform_admin.email
  scopes                 = ["userinfo-email", "cloud-platform"]

  provider = google.impersonation
}

resource "google_project_service" "enable_apis" {
  project = var.id_project
  for_each = toset(var.apis_list)
  service = each.key
}

