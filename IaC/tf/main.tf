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

# CREAMOS UN BUCKET EN GCS
resource "google_storage_bucket" "my_bucket" {
  name     = "bucket_test_ceep"
  location = "europe-west3"
}

#ACTIVAMOS TODAS LAS APIS NECESARIAS
resource "google_project_service" "DataProc_API" {
  project = var.project
  service = "dataproc.googleapis.com"
}

resource "google_project_service" "Google_Sheets_API" {
  project = var.project
  service = "sheets.googleapis.com"
}

resource "google_project_service" "Google_Drive_API" {
  project = var.project
  service = "drive.googleapis.com"
}

resource "google_project_service" "Compute_Engine_API" {
  project = var.project
  service = "compute.googleapis.com"
}

resource "google_project_service" "Cloud_DataPlex_API" {
  project = var.project
  service = "dataplex.googleapis.com"
}

resource "google_project_service" "Cloud_Build_API" {
  project = var.project
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "Cloud_Functions_API" {
  project = var.project
  service = "cloudfunctions.googleapis.com"
}

resource "google_project_service" "Eventarc_API" {
  project = var.project
  service = "eventarc.googleapis.com"
}

resource "google_project_service" "Cloud_Run_Admin_API" {
  project = var.project
  service = "run.googleapis.com"
}

resource "google_project_service" "Cloud_PUBSUB_API" {
  project = var.project
  service = "pubsub.googleapis.com"
}

resource "google_project_service" "Cloud_Logging_API" {
  project = var.project
  service = "logging.googleapis.com"
}

resource "google_project_service" "Cloud_Resource_Manager_API" {
  project = var.project
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "Secret_Manager_API" {
  project = var.project
  service = "secretmanager.googleapis.com"
}

resource "google_project_service" "Artifact_Registry_API" {
  project = var.project
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "BigQuery_Data_Transfer_API" {
  project = var.project
  service = "bigquerydatatransfer.googleapis.com"
}


resource "google_project_service" "Cloud_Datastore_API" {
  project = var.project
  service = "datastore.googleapis.com"
}

resource "google_project_service" "Cloud_OS_Login_API" {
  project = var.project
  service = "oslogin.googleapis.com"
}


resource "google_project_service" "Container_Registry_API" {
  project = var.project
  service = "containerregistry.googleapis.com"
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

# CREAR UN TEMA DE PUB/SUB
resource "google_pubsub_topic" "my_topic" {
  name = "ceep-test-topic" 
}

# CREAR UN LAKE EN DATAPLEX
resource "google_dataplex_lake" "dataplex_lake" {
  location     = "europe-west3"
  name         = "lake-test-ceep"
  # description  = "Lake for DCL"
  # display_name = "Lake for DCL"

  project = var.project
}

# MODIFICAR EL ACCESO PRIVADO A LA SUBRED
resource "google_compute_subnetwork" "default_subnetwork" {
  name          = "default"
  region        = "europe-west3"
  network       = "default" 
  ip_cidr_range = "10.156.0.0/20"

  private_ip_google_access = true
}
