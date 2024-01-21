#Proveedor
provider "google" {
  project = var.id_project
  region  = var.region
}

resource "google_cloudfunctions2_function" "drive_to_storage" {
  name          = var.name_function_drive_to_storage
  location      = var.region
  build_config {
    runtime     = var.lenguaje_programacion
    entry_point = "DriveToStorage"
    source {
      storage_source {
        bucket  = var.buckets_name
        object  = var.nombre_ubicacion_bucket_drive_to_storage
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      id_proyecto = var.id_project
      nombre_fichero_configuracion = var.nombre_fichero_conf
      topic_pubsub = var.topic_pubsub_drive_to_storage
    }
    secret_environment_variables {
      key        = var.name_secret
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    service_account_email = var.service_account
  }
}

resource "google_cloudfunctions2_function" "storage_to_drive" {
  name        = var.name_function_storage_to_drive
  location    = var.region
  build_config {
    runtime     = var.lenguaje_programacion
    entry_point = "Storage_to_Drive"
    source {
      storage_source {
        bucket = var.buckets_name
        object = var.nombre_ubicacion_bucket_storage_to_drive
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "2048M"
    available_cpu      = "1"
    timeout_seconds    = 500
    environment_variables = {
      id_proyecto = var.id_project
      nombre_fichero_configuracion = var.nombre_fichero_conf
      topic_pubsub = var.topic_pubsub_storage_to_drive
    }
    secret_environment_variables {
      key        = var.name_secret
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    service_account_email = var.service_account
  }
}

resource "google_cloudfunctions2_function" "update_scheduler" {
  name        = var.name_function_update_scheduler
  location    = var.region
  build_config {
    runtime     = var.lenguaje_programacion
    entry_point = "update_scheduler"

    source_repository {
      url = "https://github.com/tu-usuario/tu-repositorio.git"
      dir = "ruta/al/codigo"  # Ruta dentro del repositorio donde se encuentra el código de la función
    }
  }
  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    available_cpu      = "0.167"
    timeout_seconds    = 60
    environment_variables = {
      service_account_email = var.service_account
    }
    secret_environment_variables {
      key        = var.name_secret
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    service_account_email = var.service_account
  }
}