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