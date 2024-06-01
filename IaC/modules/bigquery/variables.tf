variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region_project" {
  description = "Región del proyecto"
  type        = string
}

variable "dataset_name" {
  description = "Nombre del dataset de dq"
  type        = string
}

variable "region_dataset" {
  description = "Región para despliegue del lake"
  type        = string
}
