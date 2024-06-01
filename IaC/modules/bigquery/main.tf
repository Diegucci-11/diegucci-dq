provider "google" {
  project = var.id_project
  region  = var.region_project
}

resource "google_bigquery_dataset" "dq_dataset" {
  dataset_id                  = var.dataset_name
  description                 = "Dataset for storing results of quality validations"
  location                    = var.region_dataset
}

resource "google_bigquery_table" "dq_summary" {
  dataset_id = google_bigquery_dataset.dq_dataset.dataset_id
  table_id   = "dq_summary"

  time_partitioning {
    type = "DAY"
    field = "execution_ts"
  }

  schema = <<EOF
    [
      {
        "name": "invocation_id",
        "type": "STRING"
      },
      {
        "name": "execution_ts",
        "type": "TIMESTAMP"
      },
      {
        "name": "rule_binding_id",
        "type": "STRING"
      },
      {
        "name": "rule_id",
        "type": "STRING"
      },
      {
        "name": "table_id",
        "type": "STRING"
      },
      {
        "name": "column_id",
        "type": "STRING"
      },
      {
        "name": "dimension",
        "type": "STRING"
      },
      {
        "name": "metadata_json_string",
        "type": "STRING"
      },
      {
        "name": "configs_hashsum",
        "type": "STRING"
      },
      {
        "name": "dataplex_lake",
        "type": "STRING"
      },
      {
        "name": "dataplex_zone",
        "type": "STRING"
      },
      {
        "name": "dataplex_asset_id",
        "type": "STRING"
      },
      {
        "name": "dq_run_id",
        "type": "STRING"
      },
      {
        "name": "progress_watermark",
        "type": "BOOLEAN"
      },
      {
        "name": "rows_validated",
        "type": "INTEGER"
      },
      {
        "name": "complex_rule_validation_errors_count",
        "type": "INTEGER"
      },
      {
        "name": "complex_rule_validation_success_flag",
        "type": "BOOLEAN"
      },
      {
        "name": "last_modified",
        "type": "TIMESTAMP"
      },
      {
        "name": "success_count",
        "type": "INTEGER"
      },
      {
        "name": "success_percentage",
        "type": "FLOAT"
      },
      {
        "name": "failed_count",
        "type": "INTEGER"
      },
      {
        "name": "failed_percentage",
        "type": "FLOAT"
      },
      {
        "name": "null_count",
        "type": "INTEGER"
      },
      {
        "name": "null_percentage",
        "type": "FLOAT"
      },
      {
        "name": "failed_records_query",
        "type": "STRING"
      }
    ]
  EOF
}

resource "google_bigquery_table" "dq_summary_errors" {
  dataset_id = google_bigquery_dataset.dq_dataset.dataset_id
  table_id   = "dq_summary_errors"

  time_partitioning {
    type = "DAY"
    field = "execution_ts"
  }

  schema = <<EOF
    [
      {
        "name": "invocation_id",
        "type": "STRING"
      },
      {
        "name": "execution_ts",
        "type": "TIMESTAMP"
      },
      {
        "name": "rule_binding_id",
        "type": "STRING"
      },
      {
        "name": "rule_id",
        "type": "STRING"
      },
      {
        "name": "table_id",
        "type": "STRING"
      },
      {
        "name": "column_id",
        "type": "STRING"
      },
      {
        "name": "dimension",
        "type": "STRING"
      },
      {
        "name": "metadata_json_string",
        "type": "STRING"
      },
      {
        "name": "configs_hashsum",
        "type": "STRING"
      },
      {
        "name": "dataplex_lake",
        "type": "STRING"
      },
      {
        "name": "dataplex_zone",
        "type": "STRING"
      },
      {
        "name": "dataplex_asset_id",
        "type": "STRING"
      },
      {
        "name": "dq_run_id",
        "type": "STRING"
      },
      {
        "name": "progress_watermark",
        "type": "BOOLEAN"
      },
      {
        "name": "rows_validated",
        "type": "INTEGER"
      },
      {
        "name": "complex_rule_validation_errors_count",
        "type": "INTEGER"
      },
      {
        "name": "complex_rule_validation_success_flag",
        "type": "BOOLEAN"
      },
      {
        "name": "last_modified",
        "type": "TIMESTAMP"
      },
      {
        "name": "success_count",
        "type": "INTEGER"
      },
      {
        "name": "success_percentage",
        "type": "FLOAT"
      },
      {
        "name": "failed_count",
        "type": "INTEGER"
      },
      {
        "name": "failed_percentage",
        "type": "FLOAT"
      },
      {
        "name": "null_count",
        "type": "INTEGER"
      },
      {
        "name": "null_percentage",
        "type": "FLOAT"
      },
      {
        "name": "failed_records_query",
        "type": "STRING"
      },
      {
        "name": "severity",
        "type": "INTEGER"
      },
      {
        "name": "action",
        "type": "INTEGER"
      }
    ]
  EOF
}

resource "google_bigquery_table" "looker_metadata_quality" {
  dataset_id = google_bigquery_dataset.dq_dataset.dataset_id
  table_id   = "looker_metadata_quality"

  schema = <<EOF
    [
      {
        "name": "proyecto",
        "type": "STRING"
      },
      {
        "name": "dataset",
        "type": "STRING"
      },
      {
        "name": "capa",
        "type": "STRING"
      },
      {
        "name": "tabla",
        "type": "STRING"
      },
      {
        "name": "description",
        "type": "INTEGER"
      },
      {
        "name": "desc_campos",
        "type": "FLOAT"
      },
      {
        "name": "has_owner",
        "type": "BOOLEAN"
      },
      {
        "name": "has_country",
        "type": "BOOLEAN"
      },
      {
        "name": "dataset_message",
        "type": "STRING"
      },
      {
        "name": "tabla_message",
        "type": "STRING"
      }
    ]
  EOF
}

# resource "google_bigquery_table" "looker_dq_summary" {
#   dataset_id = google_bigquery_dataset.dq_dataset.dataset_id
#   table_id   = "looker_dq_summary"

#   effective_labels = {
#     owner = "erik"
#     country = "spain"
#   }

#   view = {
#     query = "SELECT 
#       DATE(execution_ts) AS date,
#       REGEXP_EXTRACT(table_id, r'^(.*?)\.') AS project,
#       REGEXP_EXTRACT(table_id, r'\.(.*?)\.') AS dataset,
#       REGEXP_EXTRACT(table_id, r'\.(.*)$') AS table,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.columna'), '\"', '') AS column,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.capa'), '\"', '') AS capa,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.bu'), '\"', '') AS business_unit,
#       dimension AS dimension,
#       rule_id AS rule_id,
#       rows_validated AS rows_validated,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN rows_validated - complex_rule_validation_errors_count
#         ELSE success_count
#       END AS success_count,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN ROUND((1 - complex_rule_validation_errors_count / rows_validated) * 100, 2)
#         ELSE ROUND(success_percentage * 100, 2)
#       END AS success_percentage,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN complex_rule_validation_errors_count
#         ELSE failed_count
#       END AS failed_count,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN ROUND((complex_rule_validation_errors_count / rows_validated) * 100, 2)
#         ELSE ROUND(failed_percentage * 100, 2)
#       END AS failed_percentage,
#       failed_records_query AS failed_records_query
#     FROM `${var.dataset_name}.dq_summary`
#     "
#   }
# }

# resource "google_bigquery_table" "looker_dq_summary_errors" {
#   dataset_id = google_bigquery_dataset.dq_dataset.dataset_id
#   table_id   = "looker_dq_summary_errors"

#   effective_labels = {
#     owner = "erik"
#     country = "spain"
#   }

#   view = {
#     query = "SELECT 
#       DATE(execution_ts) AS date,
#       REGEXP_EXTRACT(table_id, r'^(.*?)\.') AS project,
#       REGEXP_EXTRACT(table_id, r'\.(.*?)\.') AS dataset,
#       REGEXP_EXTRACT(table_id, r'\.(.*)$') AS table,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.columna'), '\"', '') AS column,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.capa'), '\"', '') AS capa,
#       REPLACE(JSON_EXTRACT(metadata_json_string, '$.bu'), '\"', '') AS business_unit,
#       dimension AS dimension,
#       rule_id AS rule_id,
#       rows_validated AS rows_validated,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN rows_validated - complex_rule_validation_errors_count
#         ELSE success_count
#       END AS success_count,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN ROUND((1 - complex_rule_validation_errors_count / rows_validated) * 100, 2)
#         ELSE ROUND(success_percentage * 100, 2)
#       END AS success_percentage,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN complex_rule_validation_errors_count
#         ELSE failed_count
#       END AS failed_count,
#       CASE 
#         WHEN complex_rule_validation_success_flag THEN ROUND((complex_rule_validation_errors_count / rows_validated) * 100, 2)
#         ELSE ROUND(failed_percentage * 100, 2)
#       END AS failed_percentage,
#       severity AS severidad,
#       action AS accion,
#       failed_records_query AS failed_records_query
#     FROM `${var.dataset_name}.dq_summary_errors`
#     "
#   }
# }