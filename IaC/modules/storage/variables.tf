variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Región para despliegue"
  type        = string
}

variable "name_quality_bucket" {
  description = "Nombre del bucket para guardar yamls GCP"
  type        = string
}

variable "name_qid_bucket" {
  description = "Nombre del bucket para guardar sentencia QID GCP"
  type        = string
}

variable "name_qae_bucket" {
  description = "Nombre del bucket para guardar sentencia QAE GCP"
  type        = string
}

