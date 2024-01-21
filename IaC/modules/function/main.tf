resource "archive_file" "qae_notification_zip" {
  type        = "zip"
  output_path = "${path.module}/qae_notification.zip"
  source_dir  = "../../../QAE/qae_notification"
}

resource "google_cloudfunctions2_function" "qae_notification" {
  name          = var.name_function_qae_notification
  location      = var.region
  build_config {
    runtime     = var.programming_language
    entry_point = "qae_notification"
    source = "qae_notification.zip"
  }
  service_config {
    max_instance_count = 2
    available_memory   = "1024M"
    available_cpu      = "0.583"
    timeout_seconds    = 500
    environment_variables = {
      id_proyecto = var.id_project
      service_account_email = var.service_account
      version    = "latest"
    }
    secret_environment_variables {
      secret     = var.name_secret
    }
    ingress_settings = "ALLOW_ALL"
    service_account_email = var.service_account
  }
  
  depends_on = [archive_file.qae_notification_zip]
}
