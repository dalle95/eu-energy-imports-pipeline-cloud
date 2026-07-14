terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.21.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  credentials = file(var.credentials_file)
}
provider "google-beta" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials_file)
}

resource "google_storage_bucket" "eu-energy-imports-pipeline-raw-data-bucket" {
  name                        = var.bucket_name
  location                    = var.bucket_location
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id  = var.raw_bigquery_dataset_id
  project     = var.project
  location    = var.bigquery_location
  description = "Raw data BigQuery dataset for EU energy imports pipeline"
}

resource "google_bigquery_dataset" "staging_dataset" {
  dataset_id  = var.staging_bigquery_dataset_id
  project     = var.project
  location    = var.bigquery_location
  description = "Staging BigQuery dataset for EU energy imports pipeline"
}

resource "google_bigquery_dataset" "mart_dataset" {
  dataset_id  = var.mart_bigquery_dataset_id
  project     = var.project
  location    = var.bigquery_location
  description = "Mart BigQuery dataset for EU energy imports pipeline"
}

resource "google_dataform_repository" "eu_energy_repo" {
  provider           = google-beta
  name               = "eu-energy-imports-pipeline-repo"
  project            = var.project
  region             = var.region
  service_account    = google_service_account.dataform_sa.email
}

resource "google_service_account" "dataform_sa" {
  account_id   = "dataform-sa"
  display_name = "Service Account per Dataform"
  project      = var.project
}

resource "google_project_iam_member" "dataform_sa_bigquery" {
  project = var.project
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.dataform_sa.email}"
}

resource "google_project_iam_member" "dataform_sa_bigquery_job" {
  project = var.project
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dataform_sa.email}"
}