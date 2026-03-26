terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

provider "google" {
  credentials = file(var.gcs_credentials)
  project     = var.gcs_project
  region      = var.gcs_region
}

resource "google_storage_bucket" "ptv_metro_bucket" {
  name          = var.gcs_bucket_name
  location      = var.gcs_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "ptv_metro_dataset" {
  dataset_id = var.dataset_name
  location   = var.gcs_location
}


resource "google_bigquery_table" "service_updates_metro" {
  dataset_id =  var.dataset_name
  table_id   = var.big_query_table_name

  time_partitioning {
    type = "DAY"
    field = "entity_timestamp"
  }

  labels = {
    env = "default"
  }

  schema = <<EOF
  [
    {
      "name": "entity_id",
      "type": "STRING",
      "mode": "REQUIRED",
      "description": "Unique GTFS entity id"
    },
    {
      "name": "entity_timestamp",
      "type": "TIMESTAMP",
      "mode": "NULLABLE",
      "description": "Timestamp from the source feed"
    },
    {
      "name": "alert",
      "type": "JSON",
      "mode": "NULLABLE",
      "description": "Raw nested alert payload"
    },
    {
      "name": "ingest_timestamp",
      "type": "TIMESTAMP",
      "mode": "NULLABLE",
      "description": "Pipeline ingestion timestamp"
    }
  ]
  EOF
}