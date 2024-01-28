import functions_framework
import requests
from google.oauth2 import service_account
import gspread
import json
from google.cloud import storage
import os

@functions_framework.http
def qae_publisher(request):
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
    tablas = spreadsheet.worksheet('Tablas')
    
    dataset = tablas.cell(5, 2).value
    product_name = tablas.cell(2, 2).value
    environment = tablas.cell(3, 2).value
    project_id = tablas.cell(4, 2).value
    location = tablas.cell(6, 2).value

    output_qae = "# Autor: QAE_Publisher\n"\
    "# Modulo: QAE\n"\
    "#   - Notifica por email a los usuarios establecidos cuando ocurre algún error\n" \
    "# Version: 1.1\n"\
    "# Proyecto: " + project_id + "\n"\
    "# Entorno: " + environment + "\n"\
    "# Localizacion: " + location + "\n"\
    "# Producto: " + product_name + "\n\n\n"\
    "WITH alerts AS(\n"\
    "SELECT\n"\
    "CURRENT_DATETIME() as ts_notification\n"\
    ",array_to_string(array_agg(concat(severity) IGNORE NULLS), \"\\n\") as severity_list\n"\
    ",array_length(array_agg(severity IGNORE NULLS)) as issues_found\n"\
    "FROM `" + dataset + ".dq_summary_errors`\n"\
    "WHERE CURRENT_DATE() = date(execution_ts))\n"\
    "SELECT if(alerts.issues_found is null, \"No hay errores en la calidad de los datos\", \n"\
    "ERROR(CONCAT(CURRENT_DATETIME(), \" Se han identificado \", issues_found, \" errores de calidad. &&&\\n\", severity_list)))\n"\
    "FROM alerts;\n"
    
    print(output_qae)

    upload_blob(os.environ.get('QAE_BUCKET'), output_qae, os.environ.get('QAE_SQL'))
    return ""

def upload_blob(bucket_name, output_list, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")

