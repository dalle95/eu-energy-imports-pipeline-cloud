variable "credentials_file" {
  description = "Path to GCP service account JSON credentials file"
  type        = string
  default     = "keys/service-account.json"
}

variable "project" {
  description = "The Google Cloud project ID."
  type        = string
  default     = "eu-energy-imports-pipeline"
}

variable "region" {
  description = "The Google Cloud region used by the provider."
  type        = string
  default     = "europe-west8"
}

variable "bucket_name" {
  description = "The name of the Google Cloud Storage bucket."
  type        = string
  default     = "eu-energy-imports-pipeline-raw-data-bucket"
}

variable "bucket_location" {
  description = "The location for the storage bucket."
  type        = string
  default     = "EU"
}

variable "raw_bigquery_dataset_id" {
  description = "The ID of the raw BigQuery dataset."
  type        = string
  default     = "eu_energy_raw"
}

variable "staging_bigquery_dataset_id" {
  description = "The ID of the staging BigQuery dataset."
  type        = string
  default     = "eu_energy_staging"
}

variable "mart_bigquery_dataset_id" {
  description = "The ID of the mart BigQuery dataset."
  type        = string
  default     = "eu_energy_mart"
}

variable "bigquery_location" {
  description = "The location for the BigQuery dataset."
  type        = string
  default     = "EU"
}
