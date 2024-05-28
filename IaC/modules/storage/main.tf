provider "google" {
  project     = var.id_project
  region      = var.region_project
}

resource "google_storage_bucket" "yml_bucket" {
  name          = var.name_yml_bucket  
  location      = var.region_bucket     
  force_destroy = true               
}

resource "google_storage_bucket" "functions_bucket" {
  name          = var.name_functions_bucket  
  location      = var.region_bucket     
  force_destroy = true               
}