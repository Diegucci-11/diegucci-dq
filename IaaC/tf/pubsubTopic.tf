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

# CREAR UN TEMA DE PUB/SUB
resource "google_pubsub_topic" "my_topic" {
  name = "ceep-test-topic" 
}