from google.cloud import bigquery
import json
import functions_framework

@functions_framework.http
def config_gs(request):
    client = bigquery.Client()
    datasets = list(client.list_datasets())
    info = {}

    for dataset in datasets:
        if dataset.dataset_id in ['quality_dataset_test']:
                continue
        
        dataset_info = {}
        dataset_id = dataset.dataset_id
        dataset_ref = client.dataset(dataset_id)

        tables = list(client.list_tables(dataset_ref))
        tables_info = {}

        for table in tables:
            if table.table_id in ['dq_summary', 'dq_summary_errors']:
                continue

            table_info = {}
            table_ref = dataset_ref.table(table.table_id)
            table = client.get_table(table_ref)

            fields_info = {}
            for field in table.schema:
                fields_info[field.name] = field.field_type

            table_info['fields'] = fields_info
            tables_info[table.table_id] = table_info

        dataset_info['tables'] = tables_info
        info[dataset_id] = dataset_info

    info_json = json.dumps(info)
    print(info_json)
    return info_json
