variable "id_project" {
  description = "Id project GCP"
  type        = string
}

variable "region_project" {
  description = "Region for deployment"
  type        = string
}

variable "service_account" {
  description = "Service account"
  type        = string
}

variable "project_number" {
  description = "Número del proyecto"
  type        = string
}

# variable "name_secret" {
#   description = "Name for the secret of the service-account key"
#   type        = string
# }