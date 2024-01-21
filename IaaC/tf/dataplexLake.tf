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

# CREAR UN LAKE EN DATAPLEX
resource "google_dataplex_lake" "dataplex_lake" {
  location     = "europe-west3"
  name         = "lake-test-ceep"
  # description  = "Lake for DCL"
  # display_name = "Lake for DCL"

  project = var.project
}