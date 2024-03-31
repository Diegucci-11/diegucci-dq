provider "google" {
  project     = var.id_project
  region      = var.region
}

resource "google_storage_bucket" "yml_bucket" {
  name          = var.name_quality_bucket  
  location      = var.region     
  force_destroy = true               
}

resource "google_storage_bucket" "functions_bucket" {
  name          = var.name_functions_bucket  
  location      = var.region     
  force_destroy = true               
}