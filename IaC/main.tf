provider "google" {
  project     = var.id_project
  region      = var.region
}

locals {
  # service_accounts = {
  #   terraform_admin = {
  #     id             = "terraform-admin",
  #     email          = "terraform-admin@${var.project_id}.iam.gserviceaccount.com"
  #     roles_to_grant = []
  #   }
  # }

  services_to_enable = [
    "cloudfunctions.googleapis.com",
    "run.googl.googleapis.com",
    "iam.googleeapis.com",
    "logging.googleapis.com",
    "sheets.googleapis.com",
    "drive.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "connectors.googleapis.com",
    "pubsub.googleapis.com",
    "eventarc.googleapis.com",
    "cloudbuildapis.com",
  ]
}

# module "apis"{
#   source = "./modules/apis"
#   apis_list = var.apis_list
#   id_project = var.id_project
# }

# module "pubsub" {
#   source  = "./modules/pubsub"
#   qae_topic = var.qae_topic
#   dependencies_apis = module.apis.enabled_apis
# }

# module "service_account" {
#   source  = "./modules/service_account"
#   id_project = var.id_project
#   service_account = var.service_account
#   name_secret = var.name_secret
#   dependencies_apis = module.apis.enabled_apis
# }

# # module "storage" {
# #   source       = "./modulos/storage"
# #   id_project = var.id_project
# #   name_bucket  = var.name_bucket
# #   region       = var.region
# #   nombre_ubicacion_bucket_drive_to_storage = var.nombre_ubicacion_bucket_drive_to_storage
# #   nombre_ubicacion_bucket_storage_to_drive = var.nombre_ubicacion_bucket_storage_to_drive
# #   nombre_ubicacion_bucket_update_scheduler = var.nombre_ubicacion_bucket_update_scheduler
# #   nombre_ubicacion_local_drive_to_storage  = var.nombre_ubicacion_local_drive_to_storage
# #   nombre_ubicacion_local_storage_to_drive  = var.nombre_ubicacion_local_storage_to_drive
# #   nombre_ubicacion_local_update_scheduler  = var.nombre_ubicacion_local_update_scheduler
# # }

# module "function" {
#   source       = "./modules/function"
#   id_project   = var.id_project
#   region       = var.region
#   name_function_qae_notification = var.name_function_qae_notification
#   programming_language          = var.programming_language
#   service_account                = var.service_account
#   name_secret                    = var.name_secret
#   dependencies_apis = module.apis.enabled_apis
#   dependencies_service_account = module.service_account.service_account_created
# }

