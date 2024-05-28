terraform {
  backend "gcs" {
    bucket  = "backend_dq_tfgs"
    prefix  = "tfstate-storage"
  }
}
