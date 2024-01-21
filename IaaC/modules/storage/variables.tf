variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "name_bucket" {
  description = "Nombre del bucket GCP"
  type        = string
}

variable "region" {
  description = "Región para despliegue"
  type        = string
}

variable "nombre_ubicacion_bucket_drive_to_storage"{
  description = "Ubicación donde se ubicaran los ficheros de drive to storage"
  type        = string
}

variable "nombre_ubicacion_bucket_storage_to_drive"{
  description = "Ubicación donde se ubicaran los ficheros de storage to drive"
  type        = string
}

variable "nombre_ubicacion_bucket_update_scheduler"{
  description = "Ubicación donde se ubicaran los ficheros de update scheduler"
  type        = string
}

variable "nombre_ubicacion_local_drive_to_storage"{
  description = "Ubicación local de los ficheros de drive to storage"
  type        = string
}

variable "nombre_ubicacion_local_storage_to_drive"{
  description = "Ubicación local de los ficheros de storage to drive"
  type        = string
}

variable "nombre_ubicacion_local_update_scheduler"{
  description = "Ubicación local de los ficheros de update scheduler"
  type        = string
}