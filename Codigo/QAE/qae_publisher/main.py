import functions_framework
import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
from google.cloud import secretmanager
from google.cloud import storage

@functions_framework.http
def qae_publisher(request):
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # id_drive_repo = '1hWEdMgihOB4UU6Z7q0LltyC5tQ_cSFqM'

    credentials_json = json.loads(get_password('data_quality_key'))
    credentials = service_account.Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
    client = gspread.authorize(credentials)
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, SCOPES)
    # drive = GoogleDrive(gauth)

    # dateNow_name = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    # file_name = "QAE" + dateNow_name
    # file_name = "qae_test"
    # export_qid = drive.CreateFile({'parents': [{'id': id_drive_repo}], 'title': file_name})

    spreadsheet = client.open('MatrixInput_v1.1')
    sheet = spreadsheet.worksheet('Tablas')

    nombreProducto = str(sheet.get('B2')).replace("[","").replace("]","").replace("'","")
    entornoGCP = str(sheet.get('B3')).replace("[","").replace("]","").replace("'","")
    proyectoGCP = str(sheet.get('B4')).replace("[","").replace("]","").replace("'","")
    datasetGCP = str(sheet.get('B5')).replace("[","").replace("]","").replace("'","")
    lozalizaciónGCP = str(sheet.get('B6')).replace("[","").replace("]","").replace("'","")


    output_list = "# Autor: QAE_Publisher\n"\
    "# Modulo: QAE\n"\
    "#   - Notifica por email a los usuarios establecidos cuando ocurre algún error\n" \
    "# Version: 1.1\n"\
    "# Proyecto: " + proyectoGCP + "\n"\
    "# Entorno: " + entornoGCP + "\n"\
    "# Localizacion: " + lozalizaciónGCP + "\n"\
    "# Producto: " + nombreProducto + "\n\n\n"\
    "WITH alerts AS(\n"\
    "SELECT\n"\
    "CURRENT_DATETIME() as ts_notification\n"\
    ",array_to_string(array_agg(concat(severity) IGNORE NULLS), \"\\n\") as severity_list\n"\
    ",array_length(array_agg(severity IGNORE NULLS)) as issues_found\n"\
    "FROM `" + datasetGCP + ".dq_summary_errors`\n"\
    "WHERE CURRENT_DATE() = date(execution_ts))\n"\
    "SELECT if(alerts.issues_found is null, \"No hay errores en la calidad de los datos\", \n"\
    "ERROR(CONCAT(CURRENT_DATETIME(), \" Se han identificado \", issues_found, \" errores de calidad. &&&\\n\", severity_list)))\n"\
    "FROM alerts;\n"

    bucket_name = "qae_bucket"
    destination_blob_name = "qae_test"

    upload_blob(bucket_name, output_list, destination_blob_name)

    # export_qid.SetContentString(output_list)
    # export_qid.Upload()
    # with open(file_name, 'w') as f:
    #     f.write(output_list)
    return ""

def get_password(clave):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/409016403024/secrets/{clave}/versions/1"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("utf-8")

def upload_blob(bucket_name, output_list, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")

