terraform {
  backend "gcs" {
    bucket  = "backend_dq_tfg"
    prefix  = "tfstate-storage"
  }
}
