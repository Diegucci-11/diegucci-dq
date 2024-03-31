id_project = "diegucci-dq"
region = "europe-west3"
programming_language = "python311"
service_account = "dataquality"
name_secret = "data_quality_key"
name_dataplex_lake = "quality-tasks-lake"

matrix_input_file = "Matrix_Input_v2"

project_number = "409016403024"

name_function_config_gs = "config_gs_2"

name_yml_bucket = "yml_bucket"
name_functions_bucket = "functions_dq_bucket"

# bucket for tfstate
tf_backend = "tf_backend_dq"

apis_list = [
    "cloudfunctions.googleapis.com",
    "run.googleapis.com",
    "logging.googleapis.com",
    "sheets.googleapis.com",
    "drive.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "connectors.googleapis.com",
    "pubsub.googleapis.com",
    "eventarc.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
    "dataplex.googleapis.com",
    "dataproc.googleapis.com",
    "composer.googleapis.com",
  ]

# environment for composer
env_name = "env-test-1"