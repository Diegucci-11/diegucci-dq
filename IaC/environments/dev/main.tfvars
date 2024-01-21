id_project = "diegucci-dq"
number_project = ""
region = "europe-west3"
programming_language = "python311"
service_account = "dataquality"
name_secret = "data_quality_key"
qae_topic = "qae_topic"


name_function_qae_notification = ""
name_function_qae_publisher = ""
name_function_qid_publisher = ""
name_function_yml_publisher = ""

name_bucket = ""

# bucket for tfstate
tf_backend = "tf_backend_dq"


# module apis
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
  ]