variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "number_project" {
  description = "Number project GCP"
  type        = string
}

variable "region" {
  description = "Region for deployment"
  type        = string
}

variable "programming_language" {
  description = "Programming language for the cloud functions"
  type        = string
  default     = "python311"
}

variable "service_account" {
  description = "Service account"
  type        = string
}

variable "name_secret" {
  description = "Name for the secret of the service-account key"
  type        = string
}

variable "name_bucket" {
  description = "Name for the GCS bucket"
  type        = string
}

variable "tf_backend" {
  description = "Name for the tfstate bucket"
  type        = string
}
