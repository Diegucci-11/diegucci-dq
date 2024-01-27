provider "google" {
  project     = var.id_project
  region      = var.region
}

resource "google_storage_bucket" "yml_bucket" {
  name          = var.name_quality_bucket  
  location      = var.region     
  force_destroy = true               
}

resource "google_storage_bucket" "qid_bucket" {
  name          = var.name_qid_bucket  
  location      = var.region     
  force_destroy = true               
}

resource "google_storage_bucket" "qae_bucket" {
  name          = var.name_qae_bucket  
  location      = var.region     
  force_destroy = true               
}