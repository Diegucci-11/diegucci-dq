variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "name_function_qid_notification"{
  description = "Name for the qid_notification function"
  type        = string
}

variable "programming_language" {
  description = "Programming language for the cloud functions"
  type        = string
  default     = "python311"
}

variable "region" {
  description = "Region for deployment"
  type        = string
}

variable "service_account" {
  description = "Service account"
  type        = string
}

variable "name_secret" {
  description = "Name for the secret of the service-account key"
  type        = string
}

variable "dependencies_apis" {
  type    = bool
}

variable "dependencies_service_account" {
  type    = bool
}