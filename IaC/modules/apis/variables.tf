variable "apis_list"{
  description = "Required APIs for the Data Quality Platform"
  type        = list(string)
}

variable "id_project" {
  description = "Id project GCP"
  type        = string
}