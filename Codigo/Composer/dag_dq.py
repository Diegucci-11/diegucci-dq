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

actual_month = datetime.now()
month_number = actual_month.strftime('%Y%m')

DAG_ID = "dag_bigtable_tables_4"

# DATASET_BRONZE = "brz_sales_cashiers"
# DATASET_SILVER = "slv_sales_cashiers"

# BUCKET_NAME = "sales-esp-dev-dinamic-tables-sql"

BUCKET_NAME = "QAE_bucket"
BRZ_SQL_PATH = "qid_sql.sql"
SLV_SQL_PATH = "qae_sql.sql"

brz_sql = ""
slv_sql = ""

client = storage.Client()

bucket = client.bucket(BUCKET_NAME)
brz_sql = bucket.blob(BRZ_SQL_PATH).download_as_text().format(TABLE_NAME_BRZ, month_number)
slv_sql = bucket.blob(SLV_SQL_PATH).download_as_text().format(TABLE_NAME_SLV, month_number)

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
    tags=[],
) as dag:


    # descargar_task = PythonOperator(
    #     task_id='download_sql',
    #     python_callable=descargar_archivo_gcs,
    #     dag=dag,
    #     gcp_conn_id='google_cloud_storage_default',
    # )

    dataplex_task = 

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