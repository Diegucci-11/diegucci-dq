provider "google" {
  project     = var.id_project
  region      = var.region
}

# locals {
#   service_accounts = {
#     terraform_admin = {
#       id             = "terraform-admin",
#       email          = "terraform-admin@${var.id_project}.iam.gserviceaccount.com"
#       roles_to_grant = []
#     }
#   }

#   services_to_enable = [
#     "cloudfunctions.googleapis.com",
#     "run.googl.googleapis.com",
#     "iam.googleeapis.com",
#     "logging.googleapis.com",
#     "sheets.googleapis.com",
#     "drive.googleapis.com",
#     "cloudscheduler.googleapis.com",
#     "secretmanager.googleapis.com",
#     "connectors.googleapis.com",
#     "pubsub.googleapis.com",
#     "eventarc.googleapis.com",
#     "cloudbuildapis.com",
#   ]
# }

resource "google_pubsub_topic" "qae_topic" {
  name = var.qae_topic
  message_retention_duration = "604800s"
}