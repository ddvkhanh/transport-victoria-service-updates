variable "transport-vic-sv-updates-metro" {
  description = "Transport Victoria Service Updates for Metro"
  type        = string
  default     = "ptv_metro_dataset"
}

variable "gcs_storage_class" {
  description = "Storage Class"
  type        = string
  default     = "STANDARD"

}

variable "gcs_bucket_name" {
  description = "Bucket Name"
  type        = string
  default     = "ptv-bucket-kd"

}

variable "gcs_location" {
  description = "Location"
  type        = string
  default     = "australia-southeast1"
}

variable "gcs_project" {
  description = "Project"
  type        = string
  default     = "ptv-metro-service-updates"
}

variable "gcs_region" {
  description = "Region"
  type        = string
  default     = "australia-southeast1-a"
}

variable "gcs_credentials" {
  description = "Path to GCP credentials JSON file"
  type        = string
  default     = "./.gc/credentials.json"
}
