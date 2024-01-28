provider "google" {
  project     = var.id_project
  region      = var.region
}

resource "google_composer_environment" "environment_creation" {
  name   = var.env_name
  region = var.region
  config {
    software_config {
      image_version = "composer-2-airflow-2"
    }

    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
      }
      worker {
        cpu = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        min_count  = 1
        max_count  = 3
      }
    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      network    = "default"
      subnetwork = "default"
      service_account = "dataquality@diegucci-dq.iam.gserviceaccount.com"
    }
  }
}


