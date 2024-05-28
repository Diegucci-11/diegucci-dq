# Project Configuration
id_project = "diegucci-dq"
region_project = "europe-west3"
project_number = "409016403024"

# Service Account
service_account = "dataquality"
# name_secret = "data_quality_key" # NO FUNCIONA! 
# complete_email = "dataquality@diegucci-dq.iam.gserviceaccount.com" # PROBAR SI FUNCIONA LA DE ABAJO
complete_email = "${service_account}@${id_project}.iam.gserviceaccount.com"

# Dataplex Lake
name_dataplex_lake = "data-quality-lake"
region_dataplex_lake = "europe-west3"

# Cloud Functions
region_function = "europe-southwest1"
programming_language = "python311"
name_function_config_gs = "config_gs"
zip_config_gs = "config_gs.zip"
name_function_create_dag_dq = "create_dag_dq"
zip_create_dag_dq = "create_dag_dq.zip"
name_function_trigger_dag_dq = "trigger_dag_dq"
zip_trigger_dag_dq = "trigger_dag_dq.zip"

key_name = "DQ_KEY"
name_secret = "data_quality_key" # CREAR A MANO DE MOMENTO !?

matrix_input_file = "Matrix_Input_v2"

# Buckets GCS
name_yml_bucket = "yml_bucket"
name_functions_bucket = "functions_dq_bucket"
region_bucket = "europe-southwest1"

# Composer Environment
env_name = "composer-environment"
region_composer = "europe-southwest1"

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

