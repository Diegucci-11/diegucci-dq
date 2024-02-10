variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "name_function_qae_notification"{
  description = "Name for the qae_notification function"
  type        = string
}

variable "name_function_qid_publisher"{
  description = "Name for the qid_publisher function"
  type        = string
}

variable "name_function_qae_publisher"{
  description = "Name for the qae_publisher function"
  type        = string
}

variable "name_function_yml_publisher"{
  description = "Name for the yml_publisher function"
  type        = string
}

variable "name_function_config_gs"{
  description = "Name for the config_gs function"
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

variable "name_qae_bucket" {
  description = "Name for the bucket which contains the qae code"
  type        = string
}

variable "name_yml_bucket" {
  description = "Name for the bucket which contains the qae code"
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

variable "name_functions_bucket" {
  description = "name of the bucket which contains de functions code"
  type        = string
}