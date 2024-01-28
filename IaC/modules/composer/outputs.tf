output "composer_bucket_name" {
  value = google_composer_environment.environment_creation.config[0].gcs_bucket
}
