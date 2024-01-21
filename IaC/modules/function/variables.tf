#Declaramos las variables que se van a usar
variable "lenguaje_programacion" {
  description = "El lenguaje de programación de la función"
  type        = string
  default     = "Python 3.11"
}

variable "number_project" {
  description = "Nombre del proyecto GCP"
  type        = string
}

variable "buckets_name" {
  description = "Nombre del bucket en GCP"
  type        = string
}

variable "id_project" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Región para despliegue"
  type        = string
}

variable "nombre_fichero_conf" {
  description = "Nombre del fichero de configuracion"
  type        = string
}

variable "topic_pubsub_drive_to_storage" {
  description = "Nombre del tema Pub/Sub Drive to Storage"
  type        = string
}

variable "topic_pubsub_storage_to_drive" {
  description = "Nombre del tema Pub/Sub Storage to Drive"
  type        = string
}

variable "service_account" {
  description = "Cuenta de servicio"
  type        = string
}

variable "nombre_scheduler"{
  description = "Descripción que se le va a dar al scheduler"
  type        = string
}

variable "name_function_drive_to_storage"{
  description = "Nombre de la cloud function de copia desde Drive a Storage"
  type        = string
}

variable "name_function_storage_to_drive"{
  description = "Nombre de la cloud function de copia desde Storage a Drive"
  type        = string
}

variable "name_function_update_scheduler"{
  description = "Nombre de la cloud function que actualiza los scheduler"
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

variable "name_secret" {
  description = "Nombre del Secreto"
  type        = string
  default     = "clave_cuenta_datasync"
}

variable "nombre_apis" {
  description = "Nombre de las apis"
  type        = string
}