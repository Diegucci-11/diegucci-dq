from __future__ import annotations
import datetime

from airflow import models
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator

from airflow.providers.google.cloud.operators.dataplex import (
    DataplexCreateTaskOperator,
    DataplexDeleteTaskOperator,
)
from airflow.providers.google.cloud.operators.functions import (
    CloudFunctionInvokeFunctionOperator,
)

import google.auth
import json
import requests
import os
import time
from google.cloud import storage

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
    BigQueryGetDataOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryDeleteTableOperator
)

from airflow.operators.python import (
    PythonOperator,
)
import pandas_gbq
    
DAG_ID = "dag_dq_flow_8"

BUCKET_YML = "yml_bucket"
BUCKET_QID = "qid_bucket"
BUCKET_QAE = "qae_bucket"

YML = "yml_test.yml"
QID_SQL = "qid_sql.sql"
QAE_SQL = "qae_sql.sql"

client = storage.Client()

bucket_qid = client.bucket(BUCKET_QID)
bucket_qae = client.bucket(BUCKET_QAE)
qid_sql = bucket_qid.blob(QID_SQL).download_as_text()
qae_sql = bucket_qae.blob(QAE_SQL).download_as_text()


CLOUD_FUNCTION_PROJECT_ID = "diegucci-dq"
CLOUD_FUNCTION_REGION = "europe-west3"

DATAPLEX_PROJECT_ID = "diegucci-dq"
DATAPLEX_REGION = "europe-west3"
DATAPLEX_LAKE_ID = "quality-tasks-lake"
SERVICE_ACC = "dataquality@diegucci-dq.iam.gserviceaccount.com"
PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME = "dataplex-clouddq-artifacts"
SPARK_FILE_FULL_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq_pyspark_driver.py"
CLOUDDQ_EXECUTABLE_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip"
CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip.hashsum"
CONFIGS_BUCKET_NAME = BUCKET_YML
CONFIGS_PATH = f"gs://{CONFIGS_BUCKET_NAME}/{YML}"
DATAPLEX_TASK_ID = "quality-check-1"
TRIGGER_SPEC_TYPE = "ON_DEMAND"
DATAPLEX_ENDPOINT = 'https://dataplex.googleapis.com'
GCP_PROJECT_ID = "diegucci-dq"
GCP_BQ_DATASET_ID = "quality_dataset_test"
TARGET_BQ_TABLE = f"{DATAPLEX_TASK_ID}_table"
GCP_BQ_REGION = "europe-southwest1"
FULL_TARGET_TABLE_NAME = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TARGET_BQ_TABLE}"
QAE_TEMP_TABLE = "dq_qae_temp_table"

EXAMPLE_TASK_BODY = {
    "spark": {
        "python_script_file": SPARK_FILE_FULL_PATH,
        "file_uris": [CLOUDDQ_EXECUTABLE_FILE_PATH,
                      CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH,
                      CONFIGS_PATH
                      ]
    },
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

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

def qae_notification_function(data):
    if data:
        # print("Activo función!!")
        # bash_command = f"gcloud functions call qae_notification --data '{json.dumps(data)}'"
        # os.system(bash_command)
        url = 'https://europe-west3-diegucci-dq.cloudfunctions.net/qae_notification'
        data_post = {'data': data}
        data_json = json.dumps(data_post)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=data_json, headers=headers)

        if response.status_code == 200:
            print("La solicitud fue exitosa")
            print("Respuesta de la Cloud Function:", response.text)
        else:
            print("La solicitud falló con el código de estado:", response.status_code)

def yml_publisher_function():
    url = 'https://europe-west3-diegucci-dq.cloudfunctions.net/yml_publisher'
    data_post = {'data': "data"}
    data_json = json.dumps(data_post)
    headers = get_session_headers()

    response = requests.post(url, data=data_json, headers=headers)

    if response.status_code == 200:
        print("La solicitud fue exitosa")
        print("Respuesta de la Cloud Function:", response.text)
    else:
        print("La solicitud falló con el código de estado:", response.status_code)

def ejecutar_qae():
    df = pandas_gbq.read_gbq(qae_sql, project_id=GCP_PROJECT_ID, location=GCP_BQ_REGION)
    if(str(df.iloc[0, 0]).strip() == '0'):
        print("No hay errores")
    else:
        print("Envío email!")
        return df.iloc[0].tolist()
        # data = df.iloc[0].tolist()
        # invoke_function = CloudFunctionInvokeFunctionOperator(
        #     task_id="invoke_function",
        #     project_id=CLOUD_FUNCTION_PROJECT_ID,
        #     location=CLOUD_FUNCTION_REGION,
        #     input_data={"data": json.dumps(data)},
        #     function_id="qae_notification",
        # )
        # invoke_function.execute()

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
    credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/cloudfunctions"])
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

def _get_qae_state(data) -> str:
    if data: 
        return "qae_notification"
    else:
        return "sin_errores"

with models.DAG(
    DAG_ID,
    catchup=False,
    default_args=default_args,
    # schedule="0 0 1 * *",
    # start_date=datetime(2021, 1, 1)
    schedule_interval=datetime.timedelta(days=1)
    ) as dag:

    yml_publisher_f = PythonOperator(
        task_id='yml_publisher_f',
        python_callable=yml_publisher_function,
        dag=dag,
    )

    yml_publisher = CloudFunctionInvokeFunctionOperator(
        task_id="yml_publisher",
        project_id=CLOUD_FUNCTION_PROJECT_ID,
        location=CLOUD_FUNCTION_REGION,
        input_data={"data": "yml_pub"},
        function_id="yml_publisher",
    )

    qid_publisher = CloudFunctionInvokeFunctionOperator(
        task_id="qid_publisher",
        project_id=CLOUD_FUNCTION_PROJECT_ID,
        location=CLOUD_FUNCTION_REGION,
        input_data={"data": "qid_pub"},
        function_id="qid_publisher",
    )

    qae_publisher = CloudFunctionInvokeFunctionOperator(
        task_id="qae_publisher",
        project_id=CLOUD_FUNCTION_PROJECT_ID,
        location=CLOUD_FUNCTION_REGION,
        input_data={"data": "qae_pub"},
        function_id="qae_publisher",
    )

    start_op = BashOperator(
        task_id="start_task",
        bash_command="echo 'start flow'",
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

    # qid_execution = BigQueryInsertJobOperator(
    #     task_id="qid_execution",
    #     configuration={
    #         "query": {
    #             "query": qid_sql,
    #             "useLegacySql": False,
    #         }
    #     },
    #     location=GCP_BQ_REGION,
    # )

    # create_dq_qae_temp_table = BigQueryCreateEmptyTableOperator(
    #     task_id="create_dq_qae_temp_table",
    #     dataset_id=GCP_BQ_DATASET_ID,
    #     table_id=QAE_TEMP_TABLE,
    #     project_id=GCP_PROJECT_ID,
    #     schema_fields=[
    #         {"name": "ts_notification", "type": "TIMESTAMP"},
    #         {"name": "severity_list", "type": "STRING"},
    #         {"name": "issues_found", "type": "INT64"},
    #     ],
    #     # gcp_conn_id="airflow-conn-id-account",
    #     # google_cloud_storage_conn_id="airflow-conn-id",
    # )

    # qae_execution = BigQueryInsertJobOperator(
    #     task_id="qae_execution",
    #     configuration={
    #         "query": {
    #             "query": qae_sql,
    #             "useLegacySql": False,
    #             "destinationTable": {
    #                 "projectId": GCP_PROJECT_ID,
    #                 "datasetId": GCP_BQ_DATASET_ID,
    #                 "tableId": QAE_TEMP_TABLE,
    #             },
    #         }
    #     },
    #     location=GCP_BQ_REGION,
    # )

    # get_data_qae = BigQueryGetDataOperator(
    #     task_id="get_data_qae",
    #     dataset_id=GCP_BQ_DATASET_ID,
    #     table_id=QAE_TEMP_TABLE,
    #     project_id=GCP_PROJECT_ID,
    #     # max_results=100,
    #     selected_fields="severity_list",
    #     # gcp_conn_id="airflow-conn-id",
    # )

    # test = BashOperator(
    #     task_id="test",
    #     bash_command="echo CONTENIDO DE LA TABLA: {{ task_instance.xcom_pull(task_ids='get_data_qae') }}",
    #     dag=dag,
    # )

    # delete_table = BigQueryDeleteTableOperator(
    #     task_id="delete_view",
    #     deletion_dataset_table=f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{QAE_TEMP_TABLE}",
    # )
    
    # qae_task_state = BranchPythonOperator(
    #     task_id="qae_task_state",
    #     python_callable=_get_qae_state,
    #     op_kwargs={'data': "{{ ti.xcom_pull(task_ids='get_data_qae') }}"},
    #     provide_context=True,
    # )

    # sin_errores = BashOperator(
    #     task_id="sin_errores",
    #     bash_command="echo 'No hay errores de calidad'",
    #     dag=dag,
    # )
    
    # qae_notification = CloudFunctionInvokeFunctionOperator(
    #     task_id="qae_notification",
    #     project_id=CLOUD_FUNCTION_PROJECT_ID,
    #     location=CLOUD_FUNCTION_REGION,
    #     input_data={"data": json.dumps(get_data_qae.output)},
    #     function_id="qae_notification",
    # )

    # qae_execution = PythonOperator(
    #     task_id='qae_execution',
    #     python_callable=ejecutar_qae,
    #     dag=dag,
    # )

    # qae_notification_task = PythonOperator(
    #     task_id='qae_notification_task',
    #     python_callable=qae_notification,
    #     op_kwargs={'data': "{{ ti.xcom_pull(task_ids='qae_execution') }}"},
    #     dag=dag,
    # )

start_op >> yml_publisher_f >> qid_publisher >> qae_publisher >> get_dataplex_task
get_dataplex_task >> [dataplex_task_exists, dataplex_task_not_exists, dataplex_task_error]
dataplex_task_exists >> delete_dataplex_task
delete_dataplex_task >> create_dataplex_task
dataplex_task_not_exists >> create_dataplex_task
create_dataplex_task >> dataplex_task_state
dataplex_task_state >> [dataplex_task_success, dataplex_task_failed]
# dataplex_task_success >> qid_execution >> create_dq_qae_temp_table >> qae_execution >> get_data_qae >> test
# test >> qae_task_state >> [sin_errores, qae_notification]
