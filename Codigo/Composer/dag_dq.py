from __future__ import annotations
import datetime

from airflow import models
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator

from airflow.providers.google.cloud.operators.dataplex import (
    DataplexCreateTaskOperator,
    DataplexDeleteTaskOperator,
)

import google.auth
import json
import requests
import os
import time
from datetime import datetime
from google.cloud import storage

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
)

from airflow.operators.python import (
    PythonOperator,
)

# DAG_ID = "dag_dq_flow_1"

# BUCKET_YML = "yml_bucket"
# BUCKET_QID = "qid_bucket"
# BUCKET_QAE = "qae_bucket"

# YML = "yml_test.yml"
# QID_SQL = "qid_sql.sql"
# QAE_SQL = "qae_sql.sql"

# client = storage.Client()

# bucket_qid = client.bucket(BUCKET_QID)
# bucket_qae = client.bucket(BUCKET_QAE)
# qid_sql = bucket_qid.blob(QID_SQL).download_as_text()
# qae_sql = BUCKET_QAE.blob(QAE_SQL).download_as_text()

# # def recuperar_sql_gcs():
# #     client = storage.Client()

# #     bucket = client.bucket(BUCKET_NAME)
# #     brz_sql = bucket.blob(BRZ_SQL_PATH).download_as_text().format(TABLE_NAME_BRZ, month_number)
# #     slv_sql = bucket.blob(SLV_SQL_PATH).download_as_text().format(TABLE_NAME_SLV, month_number)

# # recuperar_sql_gcs()

# with DAG(
#     DAG_ID, 
#     schedule="0 0 1 * *",
#     start_date=datetime(2021, 1, 1),
#     catchup=False,
#     tags=["QID", "QAE", "Dataplex"],
# ) as dag:


#     # descargar_task = PythonOperator(
#     #     task_id='download_sql',
#     #     python_callable=descargar_archivo_gcs,
#     #     dag=dag,
#     #     gcp_conn_id='google_cloud_storage_default',
#     # )

#     # dataplex_task = 

#     qid_execution = BigQueryInsertJobOperator(
#         task_id="qid_execution",
#         configuration={
#             "query": {
#                 "query": qid_sql,
#                 "useLegacySql": False,
#             }
#         },
#         location="europe-west3",
#     )
    
#     qae_execution = BigQueryInsertJobOperator(
#         task_id="qae_execution",
#         configuration={
#             "query": {
#                 "query": qae_sql,
#                 "useLegacySql": False,
#             }
#         },
#         location="europe-west3",
#     )

#     (dataplex_task >> qid_execution >> qae_execution)














DATAPLEX_PROJECT_ID = "diegucci-dq"
DATAPLEX_REGION = "europe-west3"
DATAPLEX_LAKE_ID = "quality-tasks-lake"
SERVICE_ACC = "dataquality@diegucci-dq.iam.gserviceaccount.com"
# PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME = "your-public-bucket-with-clouddq-executable-and-hashsum" # Public Cloud Storage bucket containing the prebuilt data quality executable artifact and hashsum. There is one bucket per GCP region.
# SPARK_FILE_FULL_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq_pyspark_driver.py"
# # Public Cloud Storage bucket containing the driver code for executing data quality job. There is one bucket per GCP region.
# CLOUDDQ_EXECUTABLE_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip" # The Cloud Storage path containing the prebuilt data quality executable artifact. There is one bucket per GCP region.
# CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip.hashsum" # The Cloud Storage path containing the prebuilt data quality executable artifact hashsum. There is one bucket per GCP region.
CONFIGS_BUCKET_NAME = "yml_bucket"
CONFIGS_PATH = f"gs://{CONFIGS_BUCKET_NAME}/yml_test.yml"
DATAPLEX_TASK_ID = "task_test_1"
TRIGGER_SPEC_TYPE = "ON_DEMAND"
DATAPLEX_ENDPOINT = 'https://dataplex.googleapis.com'
GCP_PROJECT_ID = "diegucci-dq"
GCP_BQ_DATASET_ID = "Dataset_test"
TARGET_BQ_TABLE = f"{DATAPLEX_TASK_ID}_table"
GCP_BQ_REGION = "europe-west3"
FULL_TARGET_TABLE_NAME = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TARGET_BQ_TABLE}"

EXAMPLE_TASK_BODY = {
    # "spark": {
    #     "python_script_file": SPARK_FILE_FULL_PATH,
    #     "file_uris": [CLOUDDQ_EXECUTABLE_FILE_PATH,
    #                   CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH,
    #                   CONFIGS_PATH
    #                   ]
    # },
    "execution_spec": {
        "service_account": SERVICE_ACC,
        "args": {
            "TASK_ARGS": f"clouddq-executable.zip, \
                 ALL, \
                 {CONFIGS_PATH}, \
                --gcp_project_id={GCP_PROJECT_ID}, \
                --gcp_region_id={GCP_BQ_REGION}, \
                --gcp_bq_dataset_id={GCP_BQ_DATASET_ID}, \
                --target_bigquery_summary_table={FULL_TARGET_TABLE_NAME}"
        }
    },
    "trigger_spec": {
        "type_": TRIGGER_SPEC_TYPE
    },
    "description": "Clouddq Airflow Task"
}

# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

# default arguments for the dag
default_args = {
    'owner': 'Clouddq Airflow task Example',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}


def get_session_headers() -> dict:
    credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_req = google.auth.transport.requests.Request()

    credentials.refresh(auth_req)
    auth_token = credentials.token

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }

    return headers


def get_clouddq_task_status() -> str:
    headers = get_session_headers()
    res = requests.get(
        f"{DATAPLEX_ENDPOINT}/v1/projects/{DATAPLEX_PROJECT_ID}/locations/{DATAPLEX_REGION}/lakes/{DATAPLEX_LAKE_ID}/tasks/{DATAPLEX_TASK_ID}/jobs",
        headers=headers)
    print(res.status_code)
    print(res.text)
    resp_obj = json.loads(res.text)
    if res.status_code == 200:
        if (
                "jobs" in resp_obj
                and len(resp_obj["jobs"]) > 0
                and "state" in resp_obj["jobs"][0]
        ):
            task_status = resp_obj["jobs"][0]["state"]
            return task_status
    else:
        return "FAILED"


def _get_dataplex_job_state() -> str:
    task_status = get_clouddq_task_status()
    while (task_status != 'SUCCEEDED' and task_status != 'FAILED' and task_status != 'CANCELLED'
           and task_status != 'ABORTED'):
        print(time.ctime())
        time.sleep(30)
        task_status = get_clouddq_task_status()
        print(f"CloudDQ task status is {task_status}")
    return task_status

def _get_dataplex_task() -> str:
    headers = get_session_headers()
    res = requests.get(
        f"{DATAPLEX_ENDPOINT}/v1/projects/{DATAPLEX_PROJECT_ID}/locations/{DATAPLEX_REGION}/lakes/{DATAPLEX_LAKE_ID}/tasks/{DATAPLEX_TASK_ID}",
        headers=headers)
    if res.status_code == 404:
        return "task_not_exist"
    elif res.status_code == 200:
        return "task_exist"
    else:
        return "ERROR"

with models.DAG(
        'clouddq_airflow_example',
        catchup=False,
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1)) as dag:
    print("v2")

    start_op = BashOperator(
        task_id="start_task",
        bash_command="echo start",
        dag=dag,
    )

    get_dataplex_task = BranchPythonOperator(
        task_id="get_dataplex_task",
        python_callable=_get_dataplex_task,
        provide_context=True
    )

    dataplex_task_exists = BashOperator(
        task_id="task_exist",
        bash_command="echo 'Task Already Exists'",
        dag=dag,
    )
    dataplex_task_not_exists = BashOperator(
        task_id="task_not_exist",
        bash_command="echo 'Task not Present'",
        dag=dag,
    )
    dataplex_task_error = BashOperator(
        task_id="ERROR",
        bash_command="echo 'Error in fetching dataplex task details'",
        dag=dag,
    )

    delete_dataplex_task = DataplexDeleteTaskOperator(
        project_id=DATAPLEX_PROJECT_ID,
        region=DATAPLEX_REGION,
        lake_id=DATAPLEX_LAKE_ID,
        dataplex_task_id=DATAPLEX_TASK_ID,
        task_id="delete_dataplex_task",
    )

    create_dataplex_task = DataplexCreateTaskOperator(
        project_id=DATAPLEX_PROJECT_ID,
        region=DATAPLEX_REGION,
        lake_id=DATAPLEX_LAKE_ID,
        body=EXAMPLE_TASK_BODY,
        dataplex_task_id=DATAPLEX_TASK_ID,
        task_id="create_dataplex_task",
        trigger_rule="none_failed_min_one_success",
    )

    dataplex_task_state = BranchPythonOperator(
        task_id="dataplex_task_state",
        python_callable=_get_dataplex_job_state,
        provide_context=True,
    )

    dataplex_task_success = BashOperator(
        task_id="SUCCEEDED",
        bash_command="echo 'Job Completed Successfully'",
        dag=dag,
    )
    dataplex_task_failed = BashOperator(
        task_id="FAILED",
        bash_command="echo 'Job Failed'",
        dag=dag,
    )

start_op >> get_dataplex_task
get_dataplex_task >> [dataplex_task_exists, dataplex_task_not_exists, dataplex_task_error]
dataplex_task_exists >> delete_dataplex_task
delete_dataplex_task >> create_dataplex_task
dataplex_task_not_exists >> create_dataplex_task
create_dataplex_task >> dataplex_task_state
dataplex_task_state >> [dataplex_task_success, dataplex_task_failed]