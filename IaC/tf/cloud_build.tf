# DEFINICION DE VARIABLE: ID DEL PROYECTO
variable "project" {
  description = "Id del proyecto de Google Cloud"
  type        = string
  default     = "eighth-service-396109"
}

# INDICAMOS EL PROVEEDOR (GCP)
provider "google" {
  project = var.project
  credentials = file("eighth-service-396109-496d39a68911.json")
  region  = "europe-west3"
}

resource "google_cloudbuild_trigger" "filename-trigger" {
  name = "prueba2"
  location = "europe-west1"

  trigger_template {
    repo_name   = "PRUEBA"
    branch_name = "qae"
  }

  filename = "Codigo/QAE/CI-CD/cicd_qae.yaml"
}