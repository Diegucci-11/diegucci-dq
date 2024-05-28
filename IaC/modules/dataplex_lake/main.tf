provider "google" {
  project = var.id_project
  region  = var.region_project
}

resource "google_dataplex_lake" "dataplex_lake" {
  location     = var.region_dataplex_lake
  name         = var.name_dataplex_lake
  project      = var.id_project
}