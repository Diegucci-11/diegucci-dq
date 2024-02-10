id_project = "diegucci-dq"
region = "europe-west3"
programming_language = "python311"
service_account = "dataquality"
name_secret = "data_quality_key"
name_dataplex_lake = "quality-tasks-lake"

matrix_input_file = "MatrixInput_v1.1"

project_number = "409016403024"

name_function_qae_notification = "qae_notification"
name_function_qae_publisher = "qae_publisher"
name_function_qid_publisher = "qid_publisher"
name_function_yml_publisher = "yml_publisher"
name_function_config_gs = "config_gs"

name_qid_bucket = "qid_bucket"
name_qae_bucket = "qae_bucket"
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