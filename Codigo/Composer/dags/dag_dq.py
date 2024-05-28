from __future__ import annotations
import datetime
import google.auth
import json
import requests
import os
import time
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
from email.message import EmailMessage
import smtplib
from google.oauth2 import service_account
import gspread
from airflow import models
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.google.cloud.operators.dataplex import (
    DataplexCreateTaskOperator,
    DataplexDeleteTaskOperator,
)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from google.cloud import secretmanager

DAG_NAME = "dq_validation_dag_11"

YML = "yml_test.yml"

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

client = secretmanager.SecretManagerServiceClient()
name_secret = "projects/409016403024/secrets/data_quality_key/versions/latest"
response = client.access_secret_version(request={"name": name_secret})
payload = response.payload.data.decode("UTF-8")

credentials = service_account.Credentials.from_service_account_info(json.loads(payload), scopes=SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open("Matrix_Input_v2")

tablas_sheet = spreadsheet.worksheet('Tablas')
reglas_sheet = spreadsheet.worksheet('Reglas')
correos_sheet = spreadsheet.worksheet('Correos')
filtros_sheet = spreadsheet.worksheet('Filtros')

dataset = tablas_sheet.cell(5, 2).value
product_name = tablas_sheet.cell(2, 2).value
environment = tablas_sheet.cell(3, 2).value
project_id = tablas_sheet.cell(4, 2).value
location = tablas_sheet.cell(6, 2).value

DATAPLEX_PROJECT_ID = "diegucci-dq"
DATAPLEX_REGION = "europe-west3"
DATAPLEX_LAKE_ID = "quality-tasks-lake"
SERVICE_ACC = "dataquality@diegucci-dq.iam.gserviceaccount.com"
PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME = "dataplex-clouddq-artifacts"
# SPARK_FILE_FULL_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq_pyspark_driver.py"
SPARK_FILE_FULL_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}/clouddq_pyspark_driver.py"
# CLOUDDQ_EXECUTABLE_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip"
CLOUDDQ_EXECUTABLE_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}/clouddq-executable.zip"
# CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip.hashsum"
CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}/clouddq-executable.zip.hashsum"
CONFIGS_BUCKET_NAME = "yml_bucket"
CONFIGS_PATH = f"gs://{CONFIGS_BUCKET_NAME}/{YML}"
DATAPLEX_TASK_ID = "dq-v2-check-1"
TRIGGER_SPEC_TYPE = "ON_DEMAND"
DATAPLEX_ENDPOINT = 'https://dataplex.googleapis.com'
GCP_PROJECT_ID = project_id
GCP_BQ_DATASET_ID = dataset
TARGET_BQ_TABLE = f"{DATAPLEX_TASK_ID}_table"
GCP_BQ_REGION = location
# FULL_TARGET_TABLE_NAME = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TARGET_BQ_TABLE}"
FULL_TARGET_TABLE_NAME = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.dq_summary"
ERRORS_TABLE = "dq_summary_errors"

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

def yml_publisher():
    file_name = YML
    
    rules = reglas_sheet.range('H3:H')
    rules_values = [str(cell.value) for cell in rules if cell.value.strip()]

    filters = filtros_sheet.range('H3:H')
    filters_values = [str(cell.value) for cell in filters if cell.value.strip()]

    output_yaml = "rule_dimensions:\n  - Exactitud\n  - Completitud\n  - Consistencia\n  - Integridad\n  - Disponibilidad\n  - Unicidad\n  - Validez\n\n"
    
    output_yaml += "row_filters:\n\n  "
    output_yaml += "\n\n  ".join(filters_values)
    output_yaml += "\n\nrules:\n\n  "
    output_yaml += "\n\n  ".join(rules_values)
    output_yaml += "\n\nrule_bindings: \n\n"
    
    all_values_matrix_input = spreadsheet.worksheet('Matriz_Input').get_all_values()

    df_matrix = pd.DataFrame(all_values_matrix_input[2:])
    df_tablas = pd.DataFrame(tablas_sheet.get('A14:D'), columns=["Tabla", "Descripcion", "Proyecto", "Dataset"])
    df_tablas = df_tablas.loc[:, ["Proyecto", "Dataset", "Tabla"]]
    
    df = pd.merge(df_tablas, df_matrix, how="right", left_on='Tabla', right_on=0)
    df.drop(columns=['Tabla'], inplace=True)

    for indice_fila, fila in df.iloc[2:].iterrows():
        binding = ""
        if(fila.iloc[2] is not None and fila.iloc[2].strip() != ''):
            binding += "  " + fila.iloc[2].upper() + "_" + fila.iloc[3].upper() + ":\n"
            binding += f"    entity_uri: bigquery://projects/{fila.iloc[0]}/locations/{location}/datasets/{fila.iloc[1]}/tables/{fila.iloc[2]}\n"
            binding += f"    column_id: {fila.iloc[3]}\n"
            binding += f"    row_filter_id: {fila.iloc[9]}\n"
            binding += "    rule_ids:"
            for columna, valor_celda in fila[10:].items():
                if valor_celda.upper() == 'X':
                    binding += f"\n\n      - {df.iloc[0][columna]}"
                elif valor_celda is not None and valor_celda.strip() != "":
                    if df.iloc[0][columna] is not None and df.iloc[0][columna].strip() != "":
                        binding += f"\n\n      - {df.iloc[0][columna]}:\n          {df.iloc[1][columna]}: {valor_celda}"
                    else:
                        binding += f"\n          {df.iloc[1][columna]}: {valor_celda}"
            binding += "\n\n    metadata:\n"
            binding += f"      project: {project_id}\n"
            binding += f"      capa: {fila.iloc[7]}\n"
            binding += f"      bu: {fila.iloc[8]}\n\n"

        output_yaml += binding

    upload_blob(CONFIGS_BUCKET_NAME, output_yaml, file_name)

def qid_publisher():
    rules = reglas_sheet.get_all_values()
    dataFrame = pd.DataFrame(rules)
    df_reglas = dataFrame.iloc[2:, [2, 8, 9]]
    df_reglas.dropna(how='all', axis=0, inplace=True)

    output_qid = f"""
                    INSERT INTO {GCP_BQ_DATASET_ID}.{ERRORS_TABLE} select *\n
                """
    severity_list = ",CASE\n\n"
    action_list = ",CASE\n\n"
    message_list = ",CASE\n\n"
    for indice_fila, fila in df_reglas.iterrows():
      if fila.iloc[0] != "" and fila.iloc[0] is not None:
        severity_list += "WHEN rule_id = \"" + fila.iloc[0] + "\" THEN " + fila.iloc[1][0:1]  + "\n"
        action_list += "WHEN rule_id = \"" + fila.iloc[0] + "\" THEN " + fila.iloc[2][0:1]  + "\n"
        message_list += "WHEN rule_id = \"" + fila.iloc[0] + "\" THEN CONCAT(\"Hay algún error en: \"," + "table_id" + ", \" y en campo: \"," + "column_id"  + ")\n"

    severity_list += "END severity\n"
    action_list += "END action\n"
    message_list += "END message\n"
    output_qid += severity_list + action_list + message_list
    output_qid += f"FROM {dataset}.dq_summary WHERE failed_count > 0;"

    return output_qid

def qae_query():
    client = bigquery.Client()
    query = f"""
                SELECT 
                CURRENT_DATETIME() as ts_notification
                ,array_agg(DISTINCT concat(severity) IGNORE NULLS) as severity_list
                ,array_length(array_agg(severity IGNORE NULLS)) as issues_found
                FROM {dataset}.{ERRORS_TABLE}
                WHERE CURRENT_DATE() = date(execution_ts)
            """

    query_job = client.query(query)
    df = query_job.to_dataframe()
    severity = df['severity_list'].explode().tolist()
    if(len(severity)>0):
        severity = [int(x) for x in severity]
        qae_notification(severity)

def qae_notification(severidad_list):
    df_correos = pd.DataFrame(correos_sheet.get('A3:D'), columns=["nombre", "correo", "entorno", "severidad"])
    df_correos = df_correos[df_correos['severidad'].str[0].astype(int).isin(severidad_list)]
    df_correos = df_correos[df_correos['entorno']==environment]

    indices_max_severidad = df_correos.groupby('correo')['severidad'].idxmax()
    df_max_severidad = df_correos.loc[indices_max_severidad]

    for i, fila in df_max_severidad.iterrows():
        enviarCorreo(fila.iloc[0], fila.iloc[1], fila.iloc[2], fila.iloc[3], product_name)

def enviarCorreo(name, email, env, severity, product):
    subject = "Errores en la Calidad de los Datos"
    body = f"""<div style=\"max-width:600px; margin: 0 auto; padding: 20px; border: 1px solid #ffffff;\">
                    <h1>ERRORES EN LA CALIDAD DE LOS DATOS</h1>
                    <p>Hola {name},</p>
                    <p>Este es un mensaje de notificación sobre el incumplimiento de reglas de Calidad de tus datos.</p>
                    <p>Estos errores han tenido lugar en el producto: {product} y en el entorno {env}</p>
                    <p>La severidad de estas reglas llega hasta nivel: {severity}</p>
                    <p>Para consultar detenidamente los errores utiliza el siguiente <a href="www.google.com">enlace</a></p>
                </div>
                <hr />
                <div style=\"background-color: #ffffff; padding: 20px; text-align: center;\">
                    <strong>Data Quality</strong><br>
                </div>
            """

    send_email(subject, body, email)

def upload_blob(bucket_name, output_list, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")

def notify_errors(context):
    subject = f"ERROR EN EL DAG {DAG_NAME}."
    body = f"Some errors occurred during the execution of the DAG {DAG_NAME}."
    print("Se ha producido un error en la tarea:", context['task_instance'])

    send_email(subject, body, "diegucci.sautter@gmail.com")

def send_email(subject, body, email):
    email_from = "diegucci.sautter@gmail.com"
    email_to = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(email_from, "piox fhiy stqi ywrm")
        try:
            msg = EmailMessage()
            msg.set_content(body, subtype="html")
            msg['Subject'] = subject
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Cc'] = ''
            msg['Bcc'] = ''
            smtp.send_message(msg)
            smtp.close()
            print("Mensaje enviado correctamente")
        except:
            print("Error en el envio del correo!")

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

default_args = {
    'owner': 'Alcampo',
    'retries': 0,
    'start_date': YESTERDAY,
}

with models.DAG(
    DAG_NAME,
    schedule="0 0 1 * *",
    default_args=default_args,
    on_failure_callback=notify_errors,
    ) as dag:

    start_task = DummyOperator(task_id="start_task")

    create_dataset = BigQueryCreateEmptyDatasetOperator(task_id="create_dataset", dataset_id=GCP_BQ_DATASET_ID, location=GCP_BQ_REGION)

    yml_publisher_task = PythonOperator(
        task_id='yml_publisher_task',
        python_callable=yml_publisher,
        provide_context=True,
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

    qid_publisher_task = PythonOperator(
        task_id='qid_publisher_task',
        python_callable=qid_publisher,
        provide_context=True,
    )
    
    create_summary_errors = BigQueryInsertJobOperator(
        task_id="create_summary_errors",
        configuration={
            "query": {
                "query": f"""
                            CREATE TABLE IF NOT EXISTS {GCP_BQ_DATASET_ID}.{ERRORS_TABLE} (
                                invocation_id STRING,
                                execution_ts TIMESTAMP,
                                rule_binding_id	STRING,
                                rule_id	STRING,
                                table_id STRING,
                                column_id STRING,
                                dimension STRING,
                                metadata_json_string	STRING,
                                configs_hashsum	STRING,
                                dataplex_lake STRING,
                                dataplex_zone STRING,
                                dataplex_asset_id STRING,
                                dq_run_id STRING,
                                progress_watermark BOOLEAN,
                                rows_validated	INT64,
                                complex_rule_validation_errors_count INT64,
                                complex_rule_validation_success_flag BOOLEAN,
                                last_modified TIMESTAMP,
                                success_count INT64,
                                success_percentage FLOAT64,
                                failed_count INT64,
                                failed_percentage	FLOAT64,
                                null_count INT64,
                                null_percentage	FLOAT64,
                                failed_records_query STRING,
                                severity INT64,
                                action INT64,
                                message	STRING
                            );
                        """,
                "useLegacySql": False,
            }
        },
        location=GCP_BQ_REGION,
    )
    
    qid_execution = BigQueryInsertJobOperator(
        task_id="qid_execution",
        configuration={
            "query": {
                "query": qid_publisher_task.output,
                "useLegacySql": False,
            }
        },
        location=GCP_BQ_REGION,
    )

    qae_execution = PythonOperator(
        task_id='qae_execution',
        python_callable=qae_query,
        provide_context=True,
    )

# PENDIENTE DE REFACTORIZAR! 
    metadata_task = BigQueryInsertJobOperator(
        task_id="metadata_task",
        configuration={
            "query": {
                "query": """
                -- TRUNCATE TABLE diegucci-dq.quality_dataset_test.labels_view;
                --     INSERT INTO diegucci-dq.quality_dataset_test.labels_view
                        CREATE TABLE diegucci-dq.quality_dataset_test.labels_view AS 
                        SELECT 
                        table_schema as dataset_name, 
                        table_name,
                        CASE 
                            WHEN REGEXP_CONTAINS(option_value, r'STRUCT\("owner",\s*("[^"]+"[^"]*)') 
                                AND NOT REGEXP_CONTAINS(option_value, r'STRUCT\("country",\s*("[^"]+"[^"]*)') THEN true
                            ELSE false
                        END AS has_owner,
                        CASE 
                            WHEN REGEXP_CONTAINS(option_value, r'STRUCT\("country",\s*("[^"]+"[^"]*)') 
                                AND NOT REGEXP_CONTAINS(option_value, r'STRUCT\("owner",\s*("[^"]+"[^"]*)') THEN true
                            ELSE false
                        END AS has_country
                        FROM 
                        `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLE_OPTIONS`
                        WHERE 
                        option_name = 'labels';

                -- TRUNCATE TABLE diegucci-dq.quality_dataset_test.nomenclature_view;
                --    INSERT INTO diegucci-dq.quality_dataset_test.nomenclature_view
                    CREATE TABLE diegucci-dq.quality_dataset_test.nomenclature_view AS 
                        WITH dataset_validation AS (
                        SELECT
                            SCHEMA_NAME AS dataset_name,
                            '-' AS table_name,
                            CASE 
                            WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'^esp') THEN 'El nombre del dataset no tiene prefijo de país.'
                            WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'(dev|test|pro)$') THEN 'El nombre del dataset no tiene sufijo de entorno.'
                            WHEN REGEXP_CONTAINS(SCHEMA_NAME, r'[A-Z0-9]') THEN 'El nombre del dataset no debe contener mayúsculas ni números.'
                            END AS message
                        FROM
                            `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.SCHEMATA`
                        ),
                        table_validation AS (
                        SELECT
                            table_schema AS dataset_name,
                            table_name AS table_name,
                            CASE 
                            WHEN REGEXP_CONTAINS(table_name, r'[A-Z0-9]') THEN 'El nombre de la tabla no debe contener mayúsculas ni números.'
                            END AS message
                        FROM
                            `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLES`
                        )
                        SELECT * FROM dataset_validation
                        WHERE message IS NOT NULL
                        UNION ALL
                        SELECT * FROM table_validation
                        WHERE message IS NOT NULL;

                -- TRUNCATE TABLE diegucci-dq.quality_dataset_test.metrics_mtdata_view;
                --    INSERT INTO diegucci-dq.quality_dataset_test.metrics_mtdata_view
                    CREATE TABLE diegucci-dq.quality_dataset_test.metrics_mtdata_view AS 
                        WITH nomenclature_dataset_count AS (
                        SELECT 
                        (SELECT COUNT (*) FROM `diegucci-dq.quality_dataset_test.nomenclature_view`
                            WHERE table_name = '-') AS datasets_ok,
                        (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.SCHEMATA`) AS total_datasets
                        ),
                        nomenclature_table_count AS (
                        SELECT 
                        (SELECT COUNT (*) FROM `diegucci-dq.quality_dataset_test.nomenclature_view`
                            WHERE table_name != '-') AS tables_ok,
                        (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLES`) AS total_tables
                        ),
                        labels_count AS (
                        SELECT 
                        (SELECT COUNT (*) FROM `diegucci-dq.quality_dataset_test.labels_view`
                            WHERE has_owner = TRUE) AS owner_false,
                        (SELECT COUNT (*) FROM `diegucci-dq.quality_dataset_test.labels_view`
                            WHERE has_country = TRUE) AS country_false,
                        (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLES`) AS total_tables
                        )
                        SELECT 
                        (SELECT ROUND((1-(datasets_ok / total_datasets)) * 100, 2) FROM nomenclature_dataset_count) AS metric_datasets_nom,
                        (SELECT ROUND((1-(tables_ok / total_tables)) * 100, 2) FROM nomenclature_table_count) AS metric_tables_nom,
                        (SELECT ROUND((owner_false / total_tables) * 100, 2) FROM labels_count) AS metric_owner,
                        (SELECT ROUND((country_false / total_tables) * 100, 2) FROM labels_count) AS metric_country;
                    
                -- TRUNCATE TABLE diegucci-dq.quality_dataset_test.decription_view;
                --    INSERT INTO diegucci-dq.quality_dataset_test.decription_view
                    CREATE TABLE diegucci-dq.quality_dataset_test.decription_view AS
                        WITH tables_slv AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.silver.INFORMATION_SCHEMA.TABLE_OPTIONS AS topt
                            WHERE topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '') AS slv_tables_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.silver.INFORMATION_SCHEMA.TABLES) AS slv_tables_total
                        ),
                        tables_gld AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.golden.INFORMATION_SCHEMA.TABLE_OPTIONS AS topt
                            WHERE topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '') AS gld_tables_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.golden.INFORMATION_SCHEMA.TABLES) AS gld_tables_total
                        ),
                        tables_brz AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.bronze.INFORMATION_SCHEMA.TABLE_OPTIONS AS topt
                            WHERE topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '') AS brz_tables_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.bronze.INFORMATION_SCHEMA.TABLES) AS brz_tables_total
                        ),
                        tables_other AS (
                        SELECT
                            (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLE_OPTIONS` AS topt
                            WHERE table_schema NOT IN ("bronze", "silver", "golden")
                            AND topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '') AS other_tables_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLES`) AS other_tables_total
                        ),
                        tables_all AS (
                        SELECT
                            (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLE_OPTIONS` AS topt
                            WHERE topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '') AS total_tables_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.TABLES`) AS tables_total
                        ),
                        fields_slv AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.silver.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS AS topt
                            WHERE topt.description IS NOT NULL AND TRIM(topt.description) != '') AS slv_fields_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.silver.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS) AS slv_fields_total
                        ),
                        fields_gld AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.golden.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS AS topt
                            WHERE topt.description IS NOT NULL AND TRIM(topt.description) != '') AS gld_fields_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.golden.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS) AS gld_fields_total
                        ),
                        fields_brz AS (
                        SELECT
                            (SELECT COUNT(*) FROM diegucci-dq.bronze.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS AS topt
                            WHERE topt.description IS NOT NULL AND TRIM(topt.description) != '') AS brz_fields_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM diegucci-dq.bronze.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS) AS brz_fields_total
                        ),
                        fields_other AS (
                        SELECT
                            (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` AS topt
                            WHERE table_schema NOT IN ("silver", "golden", "bronze")
                            AND topt.description IS NOT NULL AND TRIM(topt.description) != '') AS other_fields_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`) AS other_fields_total
                        ),
                        fields_all AS (
                        SELECT
                            (SELECT COUNT(*) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` AS topt
                            WHERE topt.description IS NOT NULL AND TRIM(topt.description) != '') AS total_fields_ok,
                            (SELECT DISTINCT COUNT(table_name) FROM `diegucci-dq.region-europe-southwest1.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`) AS fields_total
                        )
                        SELECT
                        (SELECT ROUND(slv_tables_ok / slv_tables_total * 100, 2) FROM tables_slv) AS slv_tables,
                        (SELECT ROUND(gld_tables_ok / gld_tables_total * 100, 2) FROM tables_gld) AS gld_tables,
                        (SELECT ROUND(brz_tables_ok / brz_tables_total * 100, 2) FROM tables_brz) AS brz_tables,
                        (SELECT ROUND(other_tables_ok / other_tables_total * 100, 2) FROM tables_other) AS other_tables,
                        (SELECT ROUND(total_tables_ok / tables_total * 100, 2) FROM tables_all) AS all_tables,
                        (SELECT ROUND(slv_fields_ok / slv_fields_total * 100, 2) FROM fields_slv) AS slv_fields,
                        (SELECT ROUND(gld_fields_ok / gld_fields_total * 100, 2) FROM fields_gld) AS gld_fields,
                        (SELECT ROUND(brz_fields_ok / brz_fields_total * 100, 2) FROM fields_brz) AS brz_fields,
                        (SELECT ROUND(other_fields_ok / other_fields_total * 100, 2) FROM fields_other) AS other_fields,
                        (SELECT ROUND(total_fields_ok / fields_total * 100, 2) FROM fields_all) AS all_fields;
                    """,
                "useLegacySql": False,
            }
        },
        location="europe-southwest1",
    )

    end_task = DummyOperator(task_id="end_task")

start_task >> create_dataset >> create_summary_errors
start_task >> yml_publisher_task >> get_dataplex_task >> [dataplex_task_exists, dataplex_task_not_exists, dataplex_task_error]
dataplex_task_exists >> delete_dataplex_task
delete_dataplex_task >> create_dataplex_task
dataplex_task_not_exists >> create_dataplex_task
create_dataplex_task >> dataplex_task_state
dataplex_task_state >> [dataplex_task_success, dataplex_task_failed]
dataplex_task_success >> qid_publisher_task >> qid_execution >> qae_execution >> end_task
dataplex_task_success >> metadata_task >> end_task
