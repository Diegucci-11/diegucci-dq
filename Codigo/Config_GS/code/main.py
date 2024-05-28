# from google.cloud import bigquery
# import json
# import functions_framework
# from google.oauth2 import service_account
# import gspread
# import os
# import json

# @functions_framework.http
# def config_gs(request):
#     client = bigquery.Client()
#     SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#     credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
#     client_gsheet = gspread.authorize(credentials)

#     spreadsheet = client_gsheet.open(os.environ.get('MATRIX_FILE'))
    
#     sheet = spreadsheet.worksheet('Tablas')
#     values_to_update = []

#     for dataset in client.list_datasets():
#         if dataset.dataset_id in ['quality_dataset_test']:
#             continue

#         for table in client.list_tables(dataset.reference):
#             table_ref = client.get_table(table.reference)

#             fields_info = ', '.join([field.name for field in table_ref.schema])

#             values_to_update.append([dataset.dataset_id, table.table_id, fields_info])

#     cell_range = f'B20:D'
#     sheet.update(cell_range, values_to_update)

#     return "Datos cargados"



import functions_framework
from google.cloud import bigquery
import gspread
import os
from google.auth import default

@functions_framework.http
def config_gs(request):
    request_json = request.get_json()
    project_id = request_json['project_id']
    fila = request_json['fila']
    dq_dataset = request_json['dq_dataset']
    
    print('project_id recibido:', project_id)
    print('fila recibido:', fila)
    print('dq_dataset recibido:', dq_dataset)

    client = bigquery.Client(project=project_id)
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials, _ = default(scopes=SCOPES)

    client_gsheet = gspread.authorize(credentials)

    spreadsheet = client_gsheet.open(os.environ.get('MATRIX_FILE'))
    
    sheet = spreadsheet.worksheet('Tablas')
    values_to_update = []

    for dataset in client.list_datasets():
        if dataset.dataset_id == dq_dataset:
            continue

        for table in client.list_tables(dataset.reference):
            table_ref = client.get_table(table.reference)

            fields_names = ','.join([field.name for field in table_ref.schema])
            fields_types = ','.join([field.field_type for field in table_ref.schema])

            values_to_update.append([project_id, dataset.dataset_id, table.table_id, "", fields_names, fields_types])

    cell_range = f'A{fila}:F'
    sheet.update(cell_range, values_to_update)

    return "Datos cargados"