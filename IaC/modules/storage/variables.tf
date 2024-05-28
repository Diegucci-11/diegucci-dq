variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region_project" {
  description = "Región del proyecto"
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

variable "region_bucket" {
  description = "Región del proyecto"
  type        = string
}