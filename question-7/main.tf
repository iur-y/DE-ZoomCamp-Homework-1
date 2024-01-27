terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.11.0"
    }
  }
}

provider "google" {
  project = var.project
  credentials = file(var.credentials)
}

resource "google_storage_bucket" "my_bucket" {
  name          = "my-super-unique-bucket-xdddddddd"
  location      = var.region
  storage_class = var.gcs_bucket_class
  force_destroy = true
}

resource "google_bigquery_dataset" "my_dataset" {
  dataset_id = "foo"
  location = var.region
  delete_contents_on_destroy = true
}