# Project Configuration
id_project = "tfg-dq"
region_project = "europe-southwest1"
project_number = "897334757784"

# Service Account
service_account = "dataquality"

# Dataplex Lake
name_dataplex_lake = "data-quality-lake"
region_dataplex_lake = "europe-west3"

# Cloud Functions
region_function = "europe-southwest1"
programming_language = "python311"
name_function_config_gs = "config_gs_tf"
zip_config_gs = "config_gs.zip"
name_function_create_dag_dq = "create_dag_dq_tf"
zip_create_dag_dq = "create_dag_dq.zip"
name_function_trigger_dag_dq = "trigger_dag_dq_tf"
zip_trigger_dag_dq = "trigger_dag_dq.zip"
name_function_append_rule = "append_rule_tf"
zip_append_rule = "append_rule.zip"
name_function_create_rule = "create_rule_tf"
zip_create_rule = "create_rule.zip"

matrix_input_file = "Matrix_Input_v2"

# Buckets GCS
name_yml_bucket = "yml_bucket_tfg"
name_functions_bucket = "functions_dq_tfg_bucket"
region_bucket = "europe-southwest1"

# BigQuery
dataset_name = "data_quality_bqset"
region_dataset = "europe-southwest1"

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
    "aiplatform.googleapis.com"
  ]

