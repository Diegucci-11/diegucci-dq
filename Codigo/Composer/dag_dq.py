from __future__ import annotations

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

DAG_ID = "dag_dq_flow_1"

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
qae_sql = BUCKET_QAE.blob(QAE_SQL).download_as_text()

# def recuperar_sql_gcs():
#     client = storage.Client()

#     bucket = client.bucket(BUCKET_NAME)
#     brz_sql = bucket.blob(BRZ_SQL_PATH).download_as_text().format(TABLE_NAME_BRZ, month_number)
#     slv_sql = bucket.blob(SLV_SQL_PATH).download_as_text().format(TABLE_NAME_SLV, month_number)

# recuperar_sql_gcs()

with DAG(
    DAG_ID, 
    schedule="0 0 1 * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["QID", "QAE", "Dataplex"],
) as dag:


    # descargar_task = PythonOperator(
    #     task_id='download_sql',
    #     python_callable=descargar_archivo_gcs,
    #     dag=dag,
    #     gcp_conn_id='google_cloud_storage_default',
    # )

    # dataplex_task = 

    qid_execution = BigQueryInsertJobOperator(
        task_id="qid_execution",
        configuration={
            "query": {
                "query": qid_sql,
                "useLegacySql": False,
            }
        },
        location="europe-west3",
    )
    
    qae_execution = BigQueryInsertJobOperator(
        task_id="qae_execution",
        configuration={
            "query": {
                "query": qae_sql,
                "useLegacySql": False,
            }
        },
        location="europe-west3",
    )

    (dataplex_task >> qid_execution >> qae_execution)