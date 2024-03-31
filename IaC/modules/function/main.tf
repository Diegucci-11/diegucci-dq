provider "google" {
  project     = var.id_project
  region      = var.region
}

data "archive_file" "config_gs" {
  type        = "zip"
  output_path = "config_gs.zip"
  source_dir  = "../../../Codigo/Config_GS/config_gs"
}

resource "google_storage_bucket_object" "archive_config_gs" {
  name   = "config_gs.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.config_gs.output_path
}

resource "google_cloudfunctions2_function" "config_gs" {
  name          = var.name_function_config_gs
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "config_gs"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = "config_gs.zip" # PENDIENTE DE PARAMETRIZAR
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      MATRIX_FILE   = var.matrix_input_file
    }
    secret_environment_variables {
      key        = "DQ_KEY" # PENDIENTE DE PARAMETRIZAR
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL" # PARAMETRIZAR? 
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com" # HACER DE OTRA FORMA?
  }
}