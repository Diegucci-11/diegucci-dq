output "composer_bucket_name" {
  value = google_composer_environment.environment_creation.config.gcs_bucket
}
