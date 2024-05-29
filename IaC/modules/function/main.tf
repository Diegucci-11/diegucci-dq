provider "google" {
  project     = var.id_project
  region      = var.region_project
}

# config_gs function
data "archive_file" "data_config_gs" {
  type        = "zip"
  output_path = var.zip_config_gs
  source_dir  = "../../../Codigo/gs_config/code"
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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}

# append_rule function
data "archive_file" "data_append_rule" {
  type        = "zip"
  output_path = var.zip_append_rule
  source_dir  = "../../../Codigo/append_rule/code"
}

resource "google_storage_bucket_object" "archive_append_rule" {
  name   = var.zip_append_rule
  bucket = var.name_functions_bucket
  source = data.archive_file.data_append_rule.output_path
}

resource "google_cloudfunctions2_function" "append_rule" {
  name          = var.name_function_append_rule
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "append_rule"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_append_rule
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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}

# create_rule function
data "archive_file" "data_create_rule" {
  type        = "zip"
  output_path = var.zip_create_rule
  source_dir  = "../../../Codigo/create_rule/code"
}

resource "google_storage_bucket_object" "archive_create_rule" {
  name   = var.zip_create_rule
  bucket = var.name_functions_bucket
  source = data.archive_file.data_create_rule.output_path
}

resource "google_cloudfunctions2_function" "create_rule" {
  name          = var.name_function_create_rule
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "create_rule"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_create_rule
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}

# PARA SIMPLIFICAR EL TFG
resource "google_cloudfunctions2_function_iam_member" "noauth" {
  project = var.id_project
  location  = google_cloudfunctions2_function.create_rule.location
  cloud_function = google_cloudfunctions2_function.create_rule.name
  role    = "roles/cloudfunctions.invoker"
  member  = "allUsers"
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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}