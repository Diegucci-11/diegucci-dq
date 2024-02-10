provider "google" {
  project     = var.id_project
  region      = var.region
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "qid_publisher.zip"
  source_dir  = "../../../Codigo/QID/qid_publisher"
}

resource "google_storage_bucket_object" "archive" {
  name   = "qid_publisher.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.default.output_path
}

resource "google_cloudfunctions2_function" "qid_notification" {
  name          = var.name_function_qid_notification
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "qid_publisher"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = "qid_publisher.zip" # PENDIENTE DE PARAMETRIZAR
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      QID_BUCKET    = var.name_qid_bucket
      QID_SQL       = "qid_sql.sql"
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