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

variable "name_secret" {
  description = "Name for the secret of the service-account key"
  type        = string
}

variable "name_qid_bucket" {
  description = "Name for the bucket which contains the qid code"
  type        = string
}

variable "service_account" {
  description = "email of the service account"
  type        = string
}

variable "matrix_input_file" {
  description = "name of the matrix input file"
  type        = string
}
