resource "google_pubsub_topic" "qae_topic" {
  name = var.qae_topic
  message_retention_duration = "604800s"
}

variable "dependencies_apis" {
  type    = bool
}