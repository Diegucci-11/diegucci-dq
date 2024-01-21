# Autor: CEEP_QAE_Publisher
# Modulo: QAE
#   - Notifica por email a los usuarios establecidos cuando ocurre algún error
# Version: 1.1
# MotorReglas: Core
# Proyecto: ceep-394706
# Entorno: Test
# Localizacion: europe-west3
# Producto: producto_CEEP


WITH alerts AS(
SELECT
CURRENT_DATETIME() as ts_notification
,array_to_string(array_agg(concat(severity) IGNORE NULLS), "\n") as severity_list
,array_length(array_agg(severity IGNORE NULLS)) as issues_found
FROM `conjuntopruebaceep.dq_summary_errors`
WHERE CURRENT_DATE() = date(execution_ts))
SELECT if(alerts.issues_found is null, "No hay errores en la calidad de los datos", 
ERROR(CONCAT(CURRENT_DATETIME(), " Se han identificado ", issues_found, " errores de calidad. &&&\n", severity_list)))
FROM alerts;
