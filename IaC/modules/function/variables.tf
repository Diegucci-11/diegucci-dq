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

variable "service_account" {
  description = "Email of the service account"
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

variable "name_function_append_rule"{
  description = "Name for the append_rule function"
  type        = string
}

variable "zip_append_rule" {
  description = "zip para la función append_rule"
  type        = string
}

variable "name_function_create_rule"{
  description = "Name for the create_rule function"
  type        = string
}

variable "zip_create_rule" {
  description = "zip para la función create_rule"
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

variable "zip_dq_validation" {
  description = "zip para la función dq_validation"
  type        = string
}

variable "name_function_dq_validation"{
  description = "Name for the dq_validation function"
  type        = string
}

variable "zip_schedule_validation" {
  description = "zip para la función schedule_validation"
  type        = string
}

variable "name_function_schedule_validation"{
  description = "Name for the schedule_validation function"
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