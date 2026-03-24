variable "transport-vic-sv-updates-metro" {
  description = "Transport Victoria Service Updates for Metro"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "GCS Storage Class"
  type        = string
  default     = "STANDARD"

}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  type        = string
  default     = "terraform-485110-terra-bucket"

}

variable "location" {
  description = "GCP Location"
  type        = string
  default     = "australia-southeast1"
}

variable "project" {
  description = "Project"
  type        = string
  default     = "terraform-485110"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "australia-southeast1-a"
}

variable "credentials" {
  description = "Path to GCP credentials JSON file"
  type        = string
  default     = "./.gc/credentials.json"
}
