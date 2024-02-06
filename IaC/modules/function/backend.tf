terraform {
  backend "gcs" {
    bucket  = "tf_backend_dq"
    prefix  = "tfstate-qid-function"
  }
}
