import functions_framework
import requests
import pandas as pd
from google.oauth2 import service_account
import gspread
import json
import os
from google.cloud import storage

@functions_framework.http
def qid_publisher(request):
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
    
    reglas = spreadsheet.worksheet('Reglas').get_all_values()
    dataFrame = pd.DataFrame(reglas)
    df_reglas = dataFrame.iloc[1:, [2, 8, 9]]
    df_reglas.dropna(how='all', axis=0, inplace=True)
    print(df_reglas)

    tablas = spreadsheet.worksheet('Tablas')
    datasetName = tablas.cell(5, 2).value

    output_qid = "# Autor: QID_Publisher\n"\
    "# Modulo: QID Quality Intelligence Decision\n"\
    "#   - Genera tabla dq_summary_errors con los registros que han detectado algún error\n"\
    "#   - Enriquece la tabla con columnas de severidad, acción y mensaje\n"\
    "# Version: 1.1\n"\
    "# Configuración: \n"\
    "#   - severity: 0 - LOW, 1 - MEDIUM, 2 - HIGH\n"\
    "#   - action: 0 - NOTIFY, 1 - WARNING, 2 - ALERT\n\n\n"\
    "insert into dq_summary_errors select * \n"

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
    output_qid += "FROM " + datasetName + ".dq_summary\nWHERE failed_count > 0;"

    print(output_qid)

    upload_blob(os.environ.get('QID_BUCKET'), output_qid, os.environ.get('QID_SQL'))
    return ""

def upload_blob(bucket_name, output_list, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")
