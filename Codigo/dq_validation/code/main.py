import functions_framework
import json
import requests
import os
import time
import pandas as pd
from requests.models import Response
import google.auth
from google.cloud import bigquery
from google.cloud import storage
import gspread
from google.cloud import dataplex_v1
from google.oauth2 import service_account

YML = "dq_specifications.yml"

credentials = service_account.Credentials.from_service_account_file("credenciales.json", scopes=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'])
dplex_credentials = service_account.Credentials.from_service_account_file("credenciales.json", scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/cloudfunctions"])
credenciales = service_account.Credentials.from_service_account_file("credenciales.json")

dataplex_client = dataplex_v1.DataplexServiceClient(credentials=dplex_credentials)
storage_client = storage.Client(credentials=credenciales)
bq_client = bigquery.Client(credentials=credenciales)
gs_client = gspread.authorize(credentials)

spreadsheet = gs_client.open(os.environ.get('MATRIX_FILE'))

tablas_sheet = spreadsheet.worksheet('Tablas')
reglas_sheet = spreadsheet.worksheet('Reglas')
correos_sheet = spreadsheet.worksheet('Correos')
filtros_sheet = spreadsheet.worksheet('Filtros')

dataset = tablas_sheet.cell(5, 2).value
product_name = tablas_sheet.cell(2, 2).value
environment = tablas_sheet.cell(3, 2).value
project_id = tablas_sheet.cell(4, 2).value
location = tablas_sheet.cell(6, 2).value

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAA1g9h-o0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=C3-Eh6-5Uz1eL2KmMhcFcK5b5-5rdQitIKAsrsXpWtY"

GCP_PROJECT_ID = project_id
GCP_BQ_DATASET_ID = dataset
GCP_BQ_REGION = location

DATAPLEX_PROJECT_ID = os.environ.get('PROJECT_ID')
DATAPLEX_REGION = "europe-west3"
DATAPLEX_LAKE_ID = f"data-quality-lake"
SERVICE_ACC = f"dataquality@tfg-dq.iam.gserviceaccount.com"
CONFIGS_BUCKET_NAME = f"yml_bucket_tfg"
DATAPLEX_TASK_ID = "dq-validation"
TARGET_BQ_TABLE = f"{DATAPLEX_TASK_ID}_table"
COMPLETE_TASK_NAME = f"projects/{DATAPLEX_PROJECT_ID}/locations/{DATAPLEX_REGION}/lakes/{DATAPLEX_LAKE_ID}/tasks/{DATAPLEX_TASK_ID}"

ERRORS_TABLE = "dq_summary_errors"
TABLE_MTDATA_QUALITY = "looker_metadata_quality"

FULL_TARGET_TABLE_NAME = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TARGET_BQ_TABLE}"
CONFIGS_PATH = f"gs://{CONFIGS_BUCKET_NAME}/{YML}"
TRIGGER_SPEC_TYPE = "ON_DEMAND"
DATAPLEX_ENDPOINT = 'https://dataplex.googleapis.com'
PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME = "dataplex-clouddq-artifacts"
SPARK_FILE_FULL_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq_pyspark_driver.py"
CLOUDDQ_EXECUTABLE_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip"
CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH = f"gs://{PUBLIC_CLOUDDQ_EXECUTABLE_BUCKET_NAME}-{DATAPLEX_REGION}/clouddq-executable.zip.hashsum"

@functions_framework.http
def main(request):
    print("Executing yaml_publisher...")
    tables_to_delete = yml_publisher()
    print("Yaml_publisher executed")
    if _get_dataplex_task()=="task_exist":
        print("Dataplex task exists")
        print("Deleting dataplex task...")
        delete_task()
        print("Dataplex task deleted")
        print("Creating dataplex task...")
        create_task()
        print("Dataplex task created")
    elif _get_dataplex_task()=="task_not_exist":
        print("Creating dataplex task...")
        create_task()
        print("Dataplex task created")
    else:
        raise ValueError("Error con la tarea de Dataplex")
    
    print("Monitoring dataplex task state...")
    task_status = _get_dataplex_job_state()

    if task_status != 'SUCCEEDED':
        raise ValueError("Error con la tarea de Dataplex")
    
    print("Dataplex task succeeded")
    print("Executing QID...")
    qid_publisher(tables_to_delete)
    print("QID executed")
    print("Executing metadata quality task...")
    metadata_quality()
    print("Metadata quality task executed")
    # print("Executing QAE...")
    # qae_query()
    # print("QAE executed")
    print("Proccess finished successfuly!")

    return "ok"
    

def send_text_card(title: str, subtitle: str, paragraph: str) -> Response:
    header = {"title": title, "subtitle": subtitle}
    widget = {"textParagraph": {"text": paragraph}}
    cards = [
        {
            "header": header,
            "sections": [{"widgets": [widget]}],
        },
    ]
    return requests.post(WEBHOOK_URL, json={"cards": cards})

def yml_publisher():
    file_name = YML
    tables_deletion = [TARGET_BQ_TABLE]

    rules = reglas_sheet.range('I3:J')
    rules_values = [str(cell.value) for cell in rules if cell.value.strip()]

    filters = filtros_sheet.range('E3:E')
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
            if '.' in fila.iloc[3]:
                partes = fila.iloc[3].split('.', 1)
                struct = True
                aux = fila.iloc[3].rsplit('.', 1)
                aux = aux[-1]
            else:
                struct = False
                aux = fila.iloc[3]
            
            tables_deletion.append(fila.iloc[2].upper() + "_" + aux.upper())
            tables_deletion.append(fila.iloc[0].replace('-', '_') + "__" + fila.iloc[1] + "__" + fila.iloc[2] + "__" + fila.iloc[3].split('.', 1)[0] + "_1")

            binding += "  " + fila.iloc[2].upper() + "_" + aux.upper() + ":\n"
            binding += f"    entity_uri: bigquery://projects/{fila.iloc[0]}/locations/{location}/datasets/{fila.iloc[1]}/tables/{fila.iloc[2]}\n"
            binding += f"    column_id: {partes[0] if struct else fila.iloc[3]}\n"
            binding += f"    row_filter_id: NO_FILTER\n"
            binding += "    rule_ids:"
            for columna, valor_celda in fila[9:].items():
                if valor_celda.upper() == 'X' and not struct:
                    binding += f"\n\n      - {df.iloc[0][columna]}"
                elif valor_celda.upper() == 'X' and struct:
                    binding += f"\n\n      - {df.iloc[0][columna] + '_STRUCT'}:\n          anidado: {partes[1]}"
                elif valor_celda is not None and valor_celda.strip() != "":
                    if df.iloc[0][columna] is not None and df.iloc[0][columna].strip() != "" and not struct:
                        binding += f"\n\n      - {df.iloc[0][columna]}:\n          {df.iloc[1][columna]}: {valor_celda}"
                    elif df.iloc[0][columna] is not None and df.iloc[0][columna].strip() != "" and struct:
                        binding += f"\n\n      - {df.iloc[0][columna] + '_STRUCT'}:\n          {df.iloc[1][columna]}: {valor_celda}\n          anidado: {partes[1]}"
                    else:
                        binding += f"\n          {df.iloc[1][columna]}: {valor_celda}"

            binding += "\n\n    metadata:\n"
            binding += f"      column: {fila.iloc[3]}\n"
            binding += f"      capa: {fila.iloc[7]}\n"
            binding += f"      bu: {fila.iloc[8]}\n\n"

        output_yaml += binding

    upload_blob(CONFIGS_BUCKET_NAME, output_yaml, file_name)
    return tables_deletion

def qid_publisher(tables_deletion):
    rules = reglas_sheet.get_all_values()
    dataFrame = pd.DataFrame(rules)
    df_reglas = dataFrame.iloc[2:, [1, 5, 6]]
    df_reglas.dropna(how='all', axis=0, inplace=True)

    output_qid = f"""
                    TRUNCATE TABLE {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{ERRORS_TABLE};
                    INSERT INTO {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{ERRORS_TABLE} select *\n
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
    output_qid += f"FROM {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.dq_summary WHERE failed_count > 0 or complex_rule_validation_errors_count > 0;"
    
    for table in tables_deletion:
        bq_client.delete_table(f'{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{table}', not_found_ok=True)

    bq_client.query(output_qid)

def qae_query():
    query = f"""
                SELECT 
                CURRENT_DATETIME() as ts_notification
                ,array_agg(DISTINCT concat(severity) IGNORE NULLS) as severity_list
                ,array_length(array_agg(severity IGNORE NULLS)) as issues_found
                FROM {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{ERRORS_TABLE}
                WHERE CURRENT_DATE() = date(execution_ts)
            """

    query_job = bq_client.query(query)
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
                    <p>Para consultar detenidamente los errores utiliza el siguiente <a href="https://lookerstudio.google.com/u/0/reporting/883e5753-e94c-45cf-b43f-6f892ef874c0/page/p_imr3x67q8c">enlace</a></p>
                </div>
                <hr />
                <div style=\"background-color: #ffffff; padding: 20px; text-align: center;\">
                    <strong>Data Quality</strong><br>
                </div>
            """

    send_text_card(
        title=subject,
        subtitle="",
        paragraph=body,
    )
    # send_email(subject, body, email)

def upload_blob(bucket_name, output_list, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")

def get_session_headers() -> dict:
    auth_req = google.auth.transport.requests.Request()

    dplex_credentials.refresh(auth_req)
    auth_token = dplex_credentials.token

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

def create_task():
    task = dataplex_v1.Task()
    task.name = COMPLETE_TASK_NAME
    task.spark.python_script_file = SPARK_FILE_FULL_PATH
    task.spark.file_uris = [CLOUDDQ_EXECUTABLE_FILE_PATH, CLOUDDQ_EXECUTABLE_HASHSUM_FILE_PATH, CONFIGS_PATH]
    task.trigger_spec.type_ = "ON_DEMAND"
    task.execution_spec.service_account = SERVICE_ACC
    
    args = {
        "TASK_ARGS": f"clouddq-executable.zip,ALL,{CONFIGS_PATH},--gcp_project_id={GCP_PROJECT_ID},--gcp_region_id={GCP_BQ_REGION},--gcp_bq_dataset_id={GCP_BQ_DATASET_ID},--target_bigquery_summary_table={FULL_TARGET_TABLE_NAME}"
    }
    task.execution_spec.args = args

    request = dataplex_v1.CreateTaskRequest(
        parent=f"projects/{DATAPLEX_PROJECT_ID}/locations/{DATAPLEX_REGION}/lakes/{DATAPLEX_LAKE_ID}",
        task_id=DATAPLEX_TASK_ID,
        task=task,
    )

    operation = dataplex_client.create_task(request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)

def delete_task():
    request = dataplex_v1.DeleteTaskRequest(name=COMPLETE_TASK_NAME)

    operation = dataplex_client.delete_task(request=request)
    print("Waiting for operation to complete...")
    operation.result()

def metadata_quality():

    query = f"""
            DECLARE dq_dataset STRING DEFAULT '{GCP_BQ_DATASET_ID}';

            TRUNCATE TABLE {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TABLE_MTDATA_QUALITY};
            INSERT INTO {GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{TABLE_MTDATA_QUALITY} 

            WITH tablas AS(
            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "BRONZE" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description'AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
            ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema = "{DATASET_SLV}"

            UNION ALL

            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "SILVER" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description'AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
            ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema = "{DATASET_GLD}"

            UNION ALL

            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "GOLDEN" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description'AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema = "{DATASET_FAT}"

            UNION ALL

            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "GOLDEN" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description'AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema = "{DATASET_EDM}"

            UNION ALL

            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "OTHER" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema NOT IN (dq_dataset, "{DATASET_SLV}", "{DATASET_GLD}")

            UNION ALL

            SELECT t.table_catalog AS proyecto, t.table_schema AS dataset, "OTHER" AS capa, t.table_name AS tabla,
                CASE WHEN topt.option_name = 'description' AND topt.option_value IS NOT NULL AND TRIM(topt.option_value) != '' THEN 100
                ELSE 0
            END description
            FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
            RIGHT JOIN `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                ON t.table_catalog = topt.table_catalog
            WHERE t.table_schema NOT IN ("{DATASET_FAT}", "{DATASET_EDM}")
            ),
            campos AS(
                SELECT table_schema AS dataset, table_name AS tabla, ROUND(COUNT(description)/COUNT(*), 2) AS desc_campos
                FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
                WHERE table_schema != dq_dataset
                GROUP BY table_schema, table_name

                UNION ALL 

                SELECT table_schema AS dataset, table_name AS tabla, ROUND(COUNT(description)/COUNT(*), 2) AS desc_campos
                FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
                WHERE table_schema != dq_dataset
                GROUP BY table_schema, table_name
            ),
            labels AS(
                SELECT 
                    t.table_schema as dataset, 
                    t.table_name as tabla,
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
                FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
                    RIGHT JOIN `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                    ON t.table_catalog = topt.table_catalog
                WHERE t.table_schema != dq_dataset

                UNION ALL

                SELECT 
                    t.table_schema as dataset, 
                    t.table_name as tabla,
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
                FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLE_OPTIONS` topt
                    RIGHT JOIN `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES` t
                    ON t.table_catalog = topt.table_catalog
                WHERE t.table_schema != dq_dataset
            ),
            dataset_validation AS (
                SELECT
                    SCHEMA_NAME AS dataset,
                    CASE 
                        WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'^esp') THEN 'El nombre del dataset no tiene prefijo de país.'
                        WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'(dev|uat|prd)$') THEN 'El nombre del dataset no tiene sufijo de entorno.'
                        WHEN REGEXP_CONTAINS(SCHEMA_NAME, r'[A-Z]') THEN 'El nombre del dataset no debe contener mayúsculas ni números.'
                    ELSE null
                    END AS dataset_message
                FROM`{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.SCHEMATA`
                WHERE SCHEMA_NAME != dq_dataset

                UNION ALL

                SELECT
                    SCHEMA_NAME AS dataset,
                    CASE 
                        WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'^esp') THEN 'El nombre del dataset no tiene prefijo de país.'
                        WHEN NOT REGEXP_CONTAINS(SCHEMA_NAME, r'(dev|uat|prd)$') THEN 'El nombre del dataset no tiene sufijo de entorno.'
                        WHEN REGEXP_CONTAINS(SCHEMA_NAME, r'[A-Z]') THEN 'El nombre del dataset no debe contener mayúsculas ni números.'
                    ELSE null
                    END AS dataset_message
                FROM`{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.SCHEMATA`
                WHERE SCHEMA_NAME != dq_dataset
            ),
            table_validation AS (
                SELECT
                    table_schema AS dataset,
                    table_name AS tabla,
                    CASE 
                        WHEN NOT REGEXP_CONTAINS(table_name, r'^(slv|gld|fat|edm)') THEN 'El nombre del dataset no tiene sufijo de entorno.'
                        WHEN REGEXP_CONTAINS(table_name, r'[A-Z]') THEN 'El nombre de la tabla no debe contener mayúsculas ni números.'
                    ELSE null
                    END AS tabla_message
                FROM `{GCP_PROJECT_CRTD}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES`
                WHERE table_schema != dq_dataset 

                UNION ALL

                SELECT
                    table_schema AS dataset,
                    table_name AS tabla,
                    CASE 
                        WHEN NOT REGEXP_CONTAINS(table_name, r'^(slv|gld|fat|edm)') THEN 'El nombre del dataset no tiene sufijo de entorno.'
                        WHEN REGEXP_CONTAINS(table_name, r'[A-Z]') THEN 'El nombre de la tabla no debe contener mayúsculas ni números.'
                    ELSE null
                    END AS tabla_message
                FROM `{GCP_PROJECT_FAT}.region-{GCP_BQ_REGION}.INFORMATION_SCHEMA.TABLES`
                WHERE table_schema != dq_dataset 
            ),
            nomenclature AS(
                SELECT d.dataset, tabla, dataset_message, tabla_message 
                FROM dataset_validation d RIGHT JOIN table_validation t
                ON d.dataset = t.dataset
            )
            SELECT proyecto, t.dataset, capa, t.tabla, description, desc_campos, has_owner, has_country, dataset_message, tabla_message
            FROM tablas t INNER JOIN campos c ON t.dataset = c.dataset AND t.tabla = c.tabla
            INNER JOIN labels l ON t.dataset = l.dataset AND t.tabla = l.tabla
            INNER JOIN nomenclature n ON t.dataset = n.dataset AND t.tabla = n.tabla;
        """
    bq_client.query(query)

