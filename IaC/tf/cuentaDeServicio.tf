# DEFINICION DE VARIABLE: ID DEL PROYECTO
variable "project" {
  description = "Id del proyecto de Google Cloud"
  type        = string
  default     = "eighth-service-396109"
}

# INDICAMOS EL PROVEEDOR (GCP)
provider "google" {
  project = var.project
  region  = "europe-west3"
}

# CREAMOS UNA CUENTA DE SERVICIO
resource "google_service_account" "cuentaservicio-ceeptest" {
  account_id   = "cuentaservicio-ceeptest"
  display_name = "CEEP Service Account Test"
}


# DAMOS PERMISOS A LA CUENTA DE SERVICIO
resource "google_project_iam_member" "editor_role" {
  project = var.project
  role    = "roles/editor"  # Puedes usar otros roles según tus necesidades
  member  = "serviceAccount:${google_service_account.cuentaservicio-ceeptest.email}"
}

resource "google_project_iam_member" "token_creator_role" {
  project = var.project
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:${google_service_account.cuentaservicio-ceeptest.email}"
}

resource "google_project_iam_member" "secret_accessor_role" {
  project = var.project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cuentaservicio-ceeptest.email}"
}

# CREAR UNA CLAVE PARA LA CUENTA DE SERVICIO
resource "google_service_account_key" "my_service_account_key" {
  service_account_id = google_service_account.cuentaservicio-ceeptest.name
}

# GUARDAR LA CLAVE COMO SECRETO
# CREAMOS UN SECRETO CON EL NOMBRE DE 'CREDENCIALES_CEEP'
resource "google_secret_manager_secret" "my_service_account_secret" {
  secret_id = "credenciales_ceep"

  replication {
    automatic = true
  }
}

# GUARDAMOS LA CLAVE DE LA CUENTA DE SERVICIO EN EL SECRETO CREADO
resource "google_secret_manager_secret_version" "my_service_account_secret_version" {
  secret = google_secret_manager_secret.my_service_account_secret.id
  secret_data = google_service_account_key.my_service_account_key.private_key
} 