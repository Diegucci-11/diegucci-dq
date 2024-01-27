from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
import gspread
import datetime
import base64
import smtplib
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from markupsafe import escape
import re
from google.cloud import secretmanager
import functions_framework

@functions_framework.http
def yml_publisher(request):
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    dateNow_name = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    file_name = "CEEP_YML_"+dateNow_name+".yml"

    #Incluir el id del repo del drive de test donde se quiera almacenar los yaml del proyecto
    # id_drive_repo = '1hWEdMgihOB4UU6Z7q0LltyC5tQ_cSFqM'

    # credentials_json = json.loads(get_password('credenciales_ceep'))
    credentials = service_account.Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
    client = gspread.authorize(credentials)
    # gauth = GoogleAuth()
    # gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, SCOPES)
    # drive = GoogleDrive(gauth)

    spreadsheet = client.open('MatrixInput_v1.1')

    reglas = spreadsheet.worksheet('Reglas')
    rules = reglas.range('K2:K')
    for rule in rules:
        print(rule)
    
    filtros = spreadsheet.worksheet('Filtros_Aut')
    filters = filtros.range('D3:D')

    output_yaml = "rule_dimensions:\n\t- Exactitud\n\t- Completitud\n\t- Consistencia\n\t- Integridad\n\t- Disponibilidad\n\t- Unicidad\n\t- Validez\n\n"
    output_yaml += "row_filters: \n"
    for filter in filters:
        output_yaml += "\t" + filter + "\n\n"

    output_yaml += "rules: \n"
    for rule in rules:
        output_yaml += "\t" + rule + "\n\n"
    


    # Incluir el número de la pestaña de la plantilla, donde está situada "yaml_semifinal", empezando por 0
    # sheet_instance_tablas = sheet.get_worksheet(15)
    # values_list = sheet_instance_tablas.col_values(1)
    # output_list = " ".join(str(x) for x in values_list)
    # export_yaml = drive.CreateFile({'parents': [{'id': id_drive_repo}], 'title': file_name})
    # export_yaml.SetContentString(output_list)
    # export_yaml.Upload()
    # with open(file_name, 'w') as f:
    #     f.write(output_list)

    return ""

# def get_password(clave):
#     client = secretmanager.SecretManagerServiceClient()
#     secret_name = f"projects/513602888593/secrets/{clave}/versions/1"
#     response = client.access_secret_version(name=secret_name)
#     return response.payload.data.decode("utf-8")
