variable "id_project" {
  description = "Id project GCP"
  type        = string
}

# variable "number_project" {
#   description = "Number project GCP"
#   type        = string
# }

variable "region" {
  description = "Region for deployment"
  type        = string
}

variable "service_account" {
  description = "Service account"
  type        = string
}

variable "name_secret" {
  description = "Name for the secret of the service-account key"
  type        = string
}

variable "tf_backend" {
  description = "Name for the tfstate bucket"
  type        = string
}

#especifico pubsub
variable "qae_topic" {
  description = "Nombre del tema Pub/Sub Storage to Drive"
  type        = string
}

# especifico apis
variable "apis_list"{
  description = "Required APIs for the Data Quality Platform"
  type        = list(string)
}

#especifico de function
variable "name_function_qae_notification"{
  description = "Name for the qae_notification function"
  type        = string
}

variable "programming_language" {
  description = "Programming language for the cloud functions"
  type        = string
  default     = "python311"
}
