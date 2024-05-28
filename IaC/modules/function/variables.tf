variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "region_project" {
  description = "Region del proyecto"
  type        = string
}

variable "programming_language" {
  description = "Programming language for the cloud functions"
  type        = string
  default     = "python311"
}

variable "region_function" {
  description = "Region de la cloud function"
  type        = string
}

variable "complete_email" {
  description = "Complete email of the service account"
  type        = string
}

variable "name_function_config_gs"{
  description = "Name for the config_gs function"
  type        = string
}

variable "zip_config_gs" {
  description = "zip para la función config_gs"
  type        = string
}

variable "name_function_create_dag_dq"{
  description = "Name for the create_dag_dq function"
  type        = string
}

variable "zip_create_dag_dq" {
  description = "zip para la función create_dag_dq"
  type        = string
}

variable "name_function_trigger_dag_dq"{
  description = "Name for the trigger_dag_dq function"
  type        = string
}

variable "zip_trigger_dag_dq" {
  description = "zip para la función trigger_dag_dq"
  type        = string
}

variable "key_name" {
  description = "Nombre para acceder a la clave en el codigo"
  type        = string
}

variable "name_secret" {
  description = "Name for the secret of the service-account key"
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