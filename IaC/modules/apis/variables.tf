variable "apis_list"{
  description = "Required APIs for the Data Quality Platform"
  type = list(string)
  default = [
    "cloudfunctions.googleapis.com",
    "run.googleapis.com",
    "logging.googleapis.com",
    "sheets.googleapis.com",
    "drive.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "connectors.googleapis.com",
    "pubsub.googleapis.com",
    "eventarc.googleapis.com",
    "cloudbuild.googleapis.com",
  ]
}

# variable "id_project" {
#   description = "Id project GCP"
#   type        = string
# }