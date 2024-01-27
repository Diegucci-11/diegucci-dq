provider "google" {
  project = var.id_project
  region  = var.region
}

resource "google_dataplex_lake" "dataplex_lake" {
  location     = var.region
  name         = var.name_dataplex_lake

  project = var.id_project
}