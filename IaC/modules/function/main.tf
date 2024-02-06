provider "google" {
  project     = var.id_project
  region      = var.region
}

# resource "google_storage_bucket" "bucket_functions_code_asdf" {
#   name          = "functions_code_asdf"  
#   location      = var.region     
#   force_destroy = true               
# }

# resource "archive_file" "function_code_zip" {
#   type        = "zip"
#   output_path = "${path.module}/function_code.zip"
#   source_dir  = "../../../Codigo/QAE/qae_notification"
# }

# resource "google_storage_bucket_object" "qae_notification2storage" {
#   name   = "qae_notification"
#   source = "function_code.zip"
#   bucket = "functions_code_asdf" 
#   depends_on = [google_storage_bucket.bucket_functions_code_asdf]
# }

resource "google_cloudfunctions2_function" "qid_notification" {
  name          = var.name_function_qid_notification
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "qid_publisher"
    source {
      storage_source {
        bucket  = "qid_bucket" 
        object  = "qid_publisher.zip"
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      QID_BUCKET    = "qid_bucket"
      QID_SQL       = "qid_sql.sql"
      MATRIX_FILE   = "MatrixInput_v1.1"
    }
    secret_environment_variables {
      DQ_KEY = "data_quality_key:latest"
    }
    ingress_settings = "ALLOW_ALL"
    service_account_email = var.service_account
  }
}

# resource "google_cloudfunctions_function" "my_function" {
#   name        = var.name_function_qae_notification
#   runtime     = var.programming_language
#   entry_point = "qae_notification"
#   trigger_http = true

#   source_code = "/path/to/your/source/code"  # Ruta local al código fuente
# }