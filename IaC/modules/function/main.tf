provider "google" {
  project     = var.id_project
  region      = var.region_project
}

# config_gs function
data "archive_file" "data_config_gs" {
  type        = "zip"
  output_path = var.zip_config_gs
  source_dir  = "../../../Codigo/config_gs/code"
}

resource "google_storage_bucket_object" "archive_config_gs" {
  name   = var.zip_config_gs
  bucket = var.name_functions_bucket
  source = data.archive_file.data_config_gs.output_path
}

resource "google_cloudfunctions2_function" "config_gs" {
  name          = var.name_function_config_gs
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "config_gs"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_config_gs
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
      key        = var.key_name
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    # service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com" # HACER DE OTRA FORMA?
    service_account_email = var.complete_email
  }
}

# create_dag_dq function
data "archive_file" "data_create_dag_dq" {
  type        = "zip"
  output_path = var.zip_create_dag_dq
  source_dir  = "../../../Codigo/create_dag_dq/code"
}

resource "google_storage_bucket_object" "archive_create_dag_dq" {
  name   = var.zip_create_dag_dq
  bucket = var.name_functions_bucket
  source = data.archive_file.data_create_dag_dq.output_path
}

resource "google_cloudfunctions2_function" "create_dag_dq" {
  name          = var.name_function_create_dag_dq
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "create_dag_dq"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_create_dag_dq
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
      key        = var.key_name
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    # service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com" # HACER DE OTRA FORMA?
    service_account_email = var.complete_email
  }
}

# trigger_dag_dq function
data "archive_file" "data_trigger_dag_dq" {
  type        = "zip"
  output_path = var.zip_trigger_dag_dq
  source_dir  = "../../../Codigo/trigger_dag_dq/code"
}

resource "google_storage_bucket_object" "archive_trigger_dag_dq" {
  name   = var.zip_trigger_dag_dq
  bucket = var.name_functions_bucket
  source = data.archive_file.data_trigger_dag_dq.output_path
}

resource "google_cloudfunctions2_function" "trigger_dag_dq" {
  name          = var.name_function_trigger_dag_dq
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "trigger_dag_dq"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_trigger_dag_dq
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
      key        = var.key_name
      project_id = var.id_project
      secret     = var.name_secret
      version    = "latest"
    }
    ingress_settings = "ALLOW_ALL"
    # service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com" # HACER DE OTRA FORMA?
    service_account_email = var.complete_email
  }
}