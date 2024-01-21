import functions_framework
import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from markupsafe import escape
import re
from google.cloud import secretmanager

@functions_framework.http
def qid_publisher(request):

    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    id_drive_repo = '1hWEdMgihOB4UU6Z7q0LltyC5tQ_cSFqM'

    credentials_json = json.loads(get_password('credenciales_ceep'))
    credentials = service_account.Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
    client = gspread.authorize(credentials)
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, SCOPES)
    drive = GoogleDrive(gauth)

    dateNow_name = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    file_name = "QID" + dateNow_name
    export_qid = drive.CreateFile({'parents': [{'id': id_drive_repo}], 'title': file_name})

    spreadsheet = client.open('CEEP_MatrixInput_v1.0')
    sheet = spreadsheet.worksheet('Reglas')

    df = pd.DataFrame()
    for a, row in enumerate(sheet.get_all_values()):
        if row[1] != '':
            df[a] = row

    dataFrame = pd.DataFrame()
    dataFrame[0] = df.T[2]
    dataFrame[1] = df.T[8]
    dataFrame[2] = df.T[9]
    output_list = "# Autor: CEEP_QID_Publisher\n"\
    "# Modulo: QID Quality Intelligence Decision\n"\
    "#   - Genera tabla dq_summary_errors con los registros que han detectado algún error\n"\
    "#   - Enriquece la tabla con columnas de severidad, acción y mensaje\n"\
    "# Version: 1.1\n"\
    "# Configuración: \n"\
    "#   - severity: 0 - LOW, 1 - MEDIUM, 2 - HIGH\n"\
    "#   - action: 0 - NOTIFY, 1 - WARNING, 2 - ALERT\n\n\n"\
    "select *\n"\
    ",CASE\n"

    for i in range(1, len(dataFrame)):
      if dataFrame.iloc[i][0] != "":
        output_list += "WHEN rule_id = \"" + dataFrame.iloc[i][0] + "\" THEN " + dataFrame.iloc[i][1][0:1]  + "\n"

    output_list += "END severity\n,CASE\n\n"

    for i in range(1, len(dataFrame)):
      if dataFrame.iloc[i][0] != "":
        output_list += "WHEN rule_id = \"" + dataFrame.iloc[i][0] + "\" THEN " + dataFrame.iloc[i][2][0:1]  + "\n"

    output_list += "END action\n,CASE\n\n"

    for i in range(1, len(dataFrame)):
      if dataFrame.iloc[i][0] != "":
        output_list += "WHEN rule_id = \"" + dataFrame.iloc[i][0] + "\" THEN CONCAT(\"Hay algún error en: \"," + "table_id" + ", \" y en campo: \"," + "column_id"  + ")\n"

    sheet = spreadsheet.worksheet('Tablas')

    datasetName = str(sheet.get('B6'))
    datasetName = datasetName.replace("[","").replace("]","").replace("'","")

    output_list += "END message\nFROM `" + datasetName + ".dq_summary`\nWHERE failed_count > 0;"

    export_qid.SetContentString(output_list)
    export_qid.Upload()
    with open(file_name, 'w') as f:
      f.write(output_list)

    return ""

def get_password(clave):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/513602888593/secrets/{clave}/versions/1"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("utf-8")
