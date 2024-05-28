variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "region_project" {
  description = "Region del proyecto"
  type        = string
}

variable "env_name" {
  description = "Name for the environment"
  type        = string
}

variable "region_composer" {
  description = "Region del entorno de composer"
  type        = string
}

variable "complete_email" {
  description = "Email completo de la cuenta de servicio"
  type        = string
}
