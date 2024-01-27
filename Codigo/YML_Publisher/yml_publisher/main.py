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
from google.cloud import storage
import functions_framework
import pandas as pd

@functions_framework.http
def yml_publisher(request):
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    dateNow_name = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    # file_name = "YML_"+dateNow_name+".yml"
    file_name = "yml_test.yml"

    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
    
    reglas = spreadsheet.worksheet('Reglas')
    rules = reglas.range('K2:K')
    rules_values = [cell.value for cell in rules if cell.value.strip()]


    filtros = spreadsheet.worksheet('Filtros_Aut')
    filters = filtros.range('D3:D')
    filters_values = [cell.value for cell in filters if cell.value.strip()]

    output_yaml = "rule_dimensions:\n\t- Exactitud\n\t- Completitud\n\t- Consistencia\n\t- Integridad\n\t- Disponibilidad\n\t- Unicidad\n\t- Validez\n\n"
    
    output_yaml += "row_filters: \n"
    for filter in filters_values:
        output_yaml += "\t" + str(filter) + "\n\n"
    
    output_yaml += "rules: \n"
    for rule in rules_values:
        output_yaml += "\t" + str(rule) + "\n\n"
    
    output_yaml += "rule_bindings: \n"
    
    all_values_matrix_input = spreadsheet.worksheet('Matriz_Input').get_all_values()

    df = pd.DataFrame(all_values_matrix_input[2:])

    df.dropna(how='all', axis=0, inplace=True)

    tablas = spreadsheet.worksheet('Tablas')

    project_id = tablas.cell(4, 2).value
    location = "europe-southwest1" # NECESARIO?

    df_tablas = pd.DataFrame(tablas.get('B:C'))
    df_tablas.dropna(how='all', axis=0, inplace=True)

    for indice_fila, fila in df.iloc[2:].iterrows():
        binding = ""
        if(fila[0] is not None and fila[0].strip() != ''):
            dataset = "FFF"
            for i, fila_tablas in df_tablas.iterrows():
                if(fila_tablas[1] == fila[0]):
                    dataset = fila_tablas[0]
            binding += "\t" + fila[0].upper() + "_" + fila[1].upper() + ":\n"
            binding += f"\t\tentity_uri: bigquery://projects/{project_id}/locations/{location}/datasets/{dataset}/tables/{fila[0]}\n"
            binding += f"\t\tcolumn_id: {fila[1]}\n"
            binding += f"\t\trow_filter_id: {fila[7]}\n"
            binding += "\t\trule_ids:\n"
            for columna, valor_celda in fila[8:].items():
                binding += "\n"
                if valor_celda == 'x':
                    binding += f"\t\t- {df.iloc[0][columna]}\n"
                elif valor_celda is not None and valor_celda.strip() != "":
                    if df.iloc[0][columna] != "" and df.iloc[0][columna] is not None:
                        binding += f"\t\t- {df.iloc[0][columna]}:\n\t\t\t{df.iloc[1][columna]}: {valor_celda}\n"
                    else:
                        binding += f"\t\t\t{df.iloc[1][columna]}: {valor_celda}\n"
                
        binding += "\n\n\t\tmetadata:\n"
        binding += f"\t\tproject:{project_id}\n"
        binding += f"\t\tcapa:{fila[5]}\n"
        binding += f"\t\tbu:{fila[6]}\n\n"

        print(binding)
        output_yaml += binding

    # print(output_yaml)

    upload_blob(os.environ.get('YML_BUCKET'), output_yaml, file_name)
    return ""

def upload_blob(bucket_name, output_list, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(output_list)

    print(f"Archivo {destination_blob_name} subido al bucket {bucket_name}.")