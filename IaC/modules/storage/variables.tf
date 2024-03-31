variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Región para despliegue"
  type        = string
}

variable "name_yml_bucket" {
  description = "Nombre del bucket para guardar yamls GCP"
  type        = string
}

variable "name_functions_bucket" {
  description = "Nombre del bucket para guardar los códigos de las funciones"
  type        = string
}
