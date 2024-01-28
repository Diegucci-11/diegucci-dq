terraform {
  backend "gcs" {
    bucket  = "tf_backend_dq"
    prefix  = "tfstate-composer"
  }

  # required_providers {
  #   google = {
  #     source  = "hashicorp/google"
  #     version = "~> 4.0"
  #   }
  #   google-beta = {
  #     source  = "hashicorp/google-beta"
  #     version = "4.78.0"
  #   }
  # }
  # required_version = ">= 0.13"
}
