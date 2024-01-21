resource "google_storage_bucket" "bucket_terraform" {
  name          = var.name_bucket  
  location      = var.region     
  force_destroy = true               
}

resource "google_storage_bucket_object" "drive_to_storage_up" {
  name   = var.nombre_ubicacion_bucket_drive_to_storage
  source = var.nombre_ubicacion_local_drive_to_storage
  bucket = var.name_bucket
  depends_on = [google_storage_bucket.bucket_terraform]
}

resource "google_storage_bucket_object" "storage_to_drive_up" {
  name   = var.nombre_ubicacion_bucket_storage_to_drive
  source = var.nombre_ubicacion_local_storage_to_drive
  bucket = var.name_bucket
  depends_on = [google_storage_bucket.bucket_terraform]
}

resource "google_storage_bucket_object" "update_scheduler_up" {
  name   = var.nombre_ubicacion_bucket_update_scheduler
  source = var.nombre_ubicacion_local_update_scheduler
  bucket = var.name_bucket
  depends_on = [google_storage_bucket.bucket_terraform]
}