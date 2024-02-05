from google.cloud import bigquery
import json
import functions_framework
from google.oauth2 import service_account
import gspread
import os
import json
# import pandas as pd

@functions_framework.http
def config_gs(request):
    client = bigquery.Client()

    datasets = list(client.list_datasets())
    # info = {}

    # for dataset in datasets:
    #     if dataset.dataset_id in ['quality_dataset_test']:
    #             continue
        
    #     dataset_info = {}
    #     dataset_id = dataset.dataset_id
    #     dataset_ref = client.dataset(dataset_id)

        
    #     tables_info = {}

    #     for table in tables:
    #         if table.table_id in ['dq_summary', 'dq_summary_errors']:
    #             continue

    #         table_info = {}
    #         table_ref = dataset_ref.table(table.table_id)
    #         table = client.get_table(table_ref)

    #         fields_info = {}
    #         for field in table.schema:
    #             fields_info[field.name] = field.field_type

    #         table_info['fields'] = fields_info
    #         tables_info[table.table_id] = table_info

    #     dataset_info['tables'] = tables_info
    #     info[dataset_id] = dataset_info

    # info_json = json.dumps(info)
    # print(info_json)
    # return info_json

    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client_gsheet = gspread.authorize(credentials)

    spreadsheet = client_gsheet.open(os.environ.get('MATRIX_FILE'))
    
    sheet = spreadsheet.worksheet('Tablas')
    fila=20
    columna=2
    cells_to_update = []

    for dataset in client.list_datasets():
        # dataset_id = dataset.dataset_id
        # dataset_ref = client.dataset(dataset_id)
        # tables = list(client.list_tables(dataset_ref))
        for table in client.list_tables(dataset.reference):
            table_ref = client.get_table(table.reference)

            fields_info = ', '.join([field.name for field in table_ref.schema])

            cells_to_update.append((fila, columna, dataset.name))
            cells_to_update.append((fila, columna + 1, table.name))
            cells_to_update.append((fila, columna + 2, fields_info))
            fila += 1

    values_to_update = [{'range': f'B{fila}:D{fila}', 'values': [[dataset.name, table.name, fields_info]]} for fila, _, _ in cells_to_update]
    sheet.update_cells(values_to_update)

    return "hola"

    

    # for dataset in client.list_datasets():
    #     for table in client.list_tables(dataset.reference):
    #         table_ref = client.get_table(table.reference)

    #         fields_info = ', '.join([field.name for field in table_ref.schema])

    #         sheet.update_cell(fila, columna, dataset.name)
    #         sheet.update_cell(fila, columna+1, table.name)
    #         sheet.update_cell(fila, columna+2, fields_info)
    #         fila += 1

                # table_info['dataset'] = dataset_id
                # table_info['tabla'] = table.table_id
                # table_info['campos'] = fields_info

                # tables_info.append(table_info)

            # df = pd.DataFrame(tables_info)

            # sheet_name = f'Dataset - {dataset_id}'

            # worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")
            # set_with_dataframe(worksheet, df)

    # return "Todo insertado! "