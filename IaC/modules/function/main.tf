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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
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
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}

# dq_validation function
data "archive_file" "data_dq_validation" {
  type        = "zip"
  output_path = var.zip_dq_validation
  source_dir  = "../../../Codigo/dq_validation/code"
}

resource "google_storage_bucket_object" "archive_dq_validation" {
  name   = var.zip_dq_validation
  bucket = var.name_functions_bucket
  source = data.archive_file.data_dq_validation.output_path
}

resource "google_cloudfunctions2_function" "dq_validation" {
  name          = var.name_function_dq_validation
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "dq_validation"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_dq_validation
      }
    }
  }
  service_config {
    max_instance_count  = 3
    available_memory   = "512M"
    available_cpu      = "0.583"
    timeout_seconds     = 3600
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
    secret_environment_variables {
      key        = "email_password"
      project_id = var.id_project
      secret     = "email_password"
      version    = "latest"
    }
  }
}

# schedule_validation function
data "archive_file" "data_schedule_validation" {
  type        = "zip"
  output_path = var.zip_schedule_validation
  source_dir  = "../../../Codigo/schedule_dq/code"
}

resource "google_storage_bucket_object" "archive_schedule_validation" {
  name   = var.zip_schedule_validation
  bucket = var.name_functions_bucket
  source = data.archive_file.data_schedule_validation.output_path
}

resource "google_cloudfunctions2_function" "schedule_validation" {
  name          = var.name_function_schedule_validation
  location      = var.region_function
  build_config {
    runtime     = var.programming_language
    entry_point = "schedule_validation"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = var.zip_schedule_validation
      }
    }
  }
  service_config {
    ingress_settings = "ALLOW_ALL"
    service_account_email = "${var.service_account}@${var.id_project}.iam.gserviceaccount.com"
  }
}