
#project config
variable "project_id" {
  type    = string
  default = "airflow-gke-338120-352104"
}

variable "region" {
  type    = string
  default = "asia-southeast1"
}

variable "zone" {
  type    = string
  default = "asia-southeast1-b"
}

variable "terraform_service_account" {
  type    = string
  default = "terraform-personal@airflow-gke-338120-352104.iam.gserviceaccount.com"
}

#storage config
variable "bucket_location" {
  type    = string
  default = "asia-southeast1"
}


#function config
variable "runtime" {
  type    = string
  default = "python38"
}

variable "python_source" {
  type    = string
  default = "./cloud_function/test_cloud_function.zip"

}
#function to run in the source code
variable "entry_point" {
  type    = string
  default = "dataflow_trigger"
}

variable "gcs_event" {
  type    = string
  default = "google.cloud.storage.object.v1.finalized"
}
#################dataflow config
variable "worker_sa" {
  type    = string
  default = "149838564778-compute@developer.gserviceaccount.com"
}

#################bigquery config
variable "bigquery_api" {
  type    = string
  default = "bigquery.googleapis.com"
}
##################cloud build config
variable "cloud_build_api" {
  type    = string
  default = "cloudbuild.googleapis.com"
}

variable "storage_class" {
  type    = string
  default = "STANDARD"
}

variable "cloudbuild_sa" {
  type    = string
  default = "149838564778@cloudbuild.gserviceaccount.com"
}
