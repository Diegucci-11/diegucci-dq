provider "google" {
  project     = var.id_project
  region      = var.region
}

terraform {
  backend "gcs" {
    bucket  = "tf_backend_dq"
    prefix  = "data_quality_tfstate"
  }
}

module "apis"{
  source = "./modules/apis"
  # id_project = var.id_project
  # apis_list = var.apis_list
}

module "pubsub" {
  source  = "./modules/pubsub"
  qae_topic = var.qae_topic
  dependencies_apis = module.apis.enabled_apis
}

# module "storage" {
#   source       = "./modulos/storage"
#   id_project = var.id_project
#   name_bucket  = var.name_bucket
#   region       = var.region
#   nombre_ubicacion_bucket_drive_to_storage = var.nombre_ubicacion_bucket_drive_to_storage
#   nombre_ubicacion_bucket_storage_to_drive = var.nombre_ubicacion_bucket_storage_to_drive
#   nombre_ubicacion_bucket_update_scheduler = var.nombre_ubicacion_bucket_update_scheduler
#   nombre_ubicacion_local_drive_to_storage  = var.nombre_ubicacion_local_drive_to_storage
#   nombre_ubicacion_local_storage_to_drive  = var.nombre_ubicacion_local_storage_to_drive
#   nombre_ubicacion_local_update_scheduler  = var.nombre_ubicacion_local_update_scheduler
# }

# module "function" {
#   source       = "./modulos/function"
#   buckets_name = module.storage.bucket_terraform_name
#   nombre_apis  = module.apis.google_project
#   id_project   = var.id_project
#   number_project = var.number_project
#   region       = var.region
#   lenguaje_programacion          = var.lenguaje_programacion
#   nombre_fichero_conf            = var.nombre_fichero_conf
#   topic_pubsub_drive_to_storage  = var.topic_pubsub_drive_to_storage
#   topic_pubsub_storage_to_drive  = var.topic_pubsub_storage_to_drive
#   service_account                = var.service_account
#   name_function_drive_to_storage = var.name_function_drive_to_storage
#   name_function_storage_to_drive = var.name_function_storage_to_drive
#   name_function_update_scheduler = var.name_function_update_scheduler
#   nombre_ubicacion_bucket_drive_to_storage = var.nombre_ubicacion_bucket_drive_to_storage
#   nombre_ubicacion_bucket_storage_to_drive = var.nombre_ubicacion_bucket_storage_to_drive
#   nombre_ubicacion_bucket_update_scheduler = var.nombre_ubicacion_bucket_update_scheduler
#   nombre_scheduler               = var.nombre_scheduler
#   name_secret    = var.name_secret
# }

