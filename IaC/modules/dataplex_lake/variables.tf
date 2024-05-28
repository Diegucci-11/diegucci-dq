variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region_project" {
  description = "Región del proyecto"
  type        = string
}

variable "name_dataplex_lake" {
  description = "Nombre del bucket GCP"
  type        = string
}

variable "region_dataplex_lake" {
  description = "Región para despliegue del lake"
  type        = string
}
