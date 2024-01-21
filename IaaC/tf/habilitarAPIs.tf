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