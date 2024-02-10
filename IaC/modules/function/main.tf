provider "google" {
  project     = var.id_project
  region      = var.region
}

data "archive_file" "qid_publisher" {
  type        = "zip"
  output_path = "qid_publisher.zip"
  source_dir  = "../../../Codigo/QID/qid_publisher"
}

data "archive_file" "qae_publisher" {
  type        = "zip"
  output_path = "qae_publisher.zip"
  source_dir  = "../../../Codigo/QAE/qae_publisher"
}

data "archive_file" "qae_notification" {
  type        = "zip"
  output_path = "qae_notification.zip"
  source_dir  = "../../../Codigo/QAE/qae_notification"
}

data "archive_file" "yml_publisher" {
  type        = "zip"
  output_path = "yml_publisher.zip"
  source_dir  = "../../../Codigo/YML_Publisher/yml_publisher"
}

data "archive_file" "config_gs" {
  type        = "zip"
  output_path = "config_gs.zip"
  source_dir  = "../../../Codigo/Config_GS/config_gs"
}

resource "google_storage_bucket_object" "archive_qid_publisher" {
  name   = "qid_publisher.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.qid_publisher.output_path
}

resource "google_storage_bucket_object" "archive_qae_publisher" {
  name   = "qae_publisher.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.qae_publisher.output_path
}

resource "google_storage_bucket_object" "archive_qae_notification" {
  name   = "qae_notification.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.qae_notification.output_path
}

resource "google_storage_bucket_object" "archive_yml_publisher" {
  name   = "yml_publisher.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.yml_publisher.output_path
}

resource "google_storage_bucket_object" "archive_config_gs" {
  name   = "config_gs.zip"
  bucket = var.name_functions_bucket
  source = data.archive_file.config_gs.output_path
}

resource "google_cloudfunctions2_function" "yml_publisher" {
  name          = var.name_function_yml_publisher
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "yml_publisher"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = "yml_publisher.zip" # PENDIENTE DE PARAMETRIZAR
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      YML_BUCKET    = var.name_yml_bucket
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

resource "google_cloudfunctions2_function" "qid_publisher" {
  name          = var.name_function_qid_publisher
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

resource "google_cloudfunctions2_function" "qae_publisher" {
  name          = var.name_function_qae_publisher
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "qae_publisher"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = "qae_publisher.zip" # PENDIENTE DE PARAMETRIZAR
      }
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      QAE_BUCKET    = var.name_qae_bucket
      QAE_SQL       = "qae_sql.sql"
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

resource "google_cloudfunctions2_function" "qae_notification" {
  name          = var.name_function_qae_notification
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "qae_notification"
    source {
      storage_source {
        bucket  = var.name_functions_bucket
        object  = "qae_notification.zip" # PENDIENTE DE PARAMETRIZAR
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