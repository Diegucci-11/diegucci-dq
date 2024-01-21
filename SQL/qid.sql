# Autor: CEEP_QID_Publisher
# Modulo: QID Quality Intelligence Decision
#   - Genera tabla dq_summary_errors con los registros que han detectado algún error
#   - Enriquece la tabla con columnas de severidad, acción y mensaje
# Version: 1.1
# Configuración: 
#   - severity: 0 - LOW, 1 - MEDIUM, 2 - HIGH
#   - action: 0 - NOTIFY, 1 - WARNING, 2 - ALERT


select *
,CASE
WHEN rule_id = "NOT_NULL_SIMPLE" THEN 2
WHEN rule_id = "NOT_BLANK" THEN 2
WHEN rule_id = "DISTINCT_VALUES" THEN 1
WHEN rule_id = "ACCEPTED_GROUP_FIX" THEN 3
WHEN rule_id = "VALUES_ALWAYS_EXPECTED" THEN 2
WHEN rule_id = "ACCEPTED_COUNTRY_FIX" THEN 3
WHEN rule_id = "OUTOFRANGE_VS_VARIATION_OF_SAME_DAY_LW" THEN 2
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT" THEN 3
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_2" THEN 3
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_NOTSUN_NOTHOL_LAST7D" THEN 2
WHEN rule_id = "VALUE_POSITIVE" THEN 2
WHEN rule_id = "VALUE_ZERO_OR_POSITIVE" THEN 3
WHEN rule_id = "VALUE_BETWEEN_FIX_UMBRAL" THEN 2
WHEN rule_id = "VALUE_BETWEEN_MOBILE_UMBRAL" THEN 2
WHEN rule_id = "VALUE_LESS_OTHER_COLUMN" THEN 2
WHEN rule_id = "BIREADER_EQUAL_VALUES_OF_PAST_WEEKS_IN_CURRENT_WEEK" THEN 2
WHEN rule_id = "NO_REFERENTIAL_INTEGRITY_VIOLATION" THEN 2
WHEN rule_id = "NO_DUPLICATES_IN_COLUMN_GROUPS" THEN 2
WHEN rule_id = "ACCEPTED_DATE_FORMAT" THEN 2
WHEN rule_id = "ACCEPTED_DATE_RANGE" THEN 2
WHEN rule_id = "ACCEPTED_DATE_OVER_UMBRAL" THEN 3
WHEN rule_id = "ACCEPTED_DATE_LESS_UMBRAL" THEN 3
WHEN rule_id = "REGEX_VALID_DATE_1" THEN 3
WHEN rule_id = "REGEX_VALID_UPPER_STRING" THEN 3
WHEN rule_id = "VALUE_EQUAL_SUM_OTHER_COLUMNS" THEN 2
WHEN rule_id = "ACCEPTED_DATE_CUSTOM_RANGE" THEN 3
WHEN rule_id = "AVAILABLE_DAILY_DATE" THEN 3
END severity
,CASE

WHEN rule_id = "NOT_NULL_SIMPLE" THEN 1
WHEN rule_id = "NOT_BLANK" THEN 2
WHEN rule_id = "DISTINCT_VALUES" THEN 2
WHEN rule_id = "ACCEPTED_GROUP_FIX" THEN 2
WHEN rule_id = "VALUES_ALWAYS_EXPECTED" THEN 2
WHEN rule_id = "ACCEPTED_COUNTRY_FIX" THEN 2
WHEN rule_id = "OUTOFRANGE_VS_VARIATION_OF_SAME_DAY_LW" THEN 2
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT" THEN 3
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_2" THEN 3
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_NOTSUN_NOTHOL_LAST7D" THEN 2
WHEN rule_id = "VALUE_POSITIVE" THEN 2
WHEN rule_id = "VALUE_ZERO_OR_POSITIVE" THEN 2
WHEN rule_id = "VALUE_BETWEEN_FIX_UMBRAL" THEN 2
WHEN rule_id = "VALUE_BETWEEN_MOBILE_UMBRAL" THEN 2
WHEN rule_id = "VALUE_LESS_OTHER_COLUMN" THEN 2
WHEN rule_id = "BIREADER_EQUAL_VALUES_OF_PAST_WEEKS_IN_CURRENT_WEEK" THEN 0
WHEN rule_id = "NO_REFERENTIAL_INTEGRITY_VIOLATION" THEN 2
WHEN rule_id = "NO_DUPLICATES_IN_COLUMN_GROUPS" THEN 2
WHEN rule_id = "ACCEPTED_DATE_FORMAT" THEN 2
WHEN rule_id = "ACCEPTED_DATE_RANGE" THEN 2
WHEN rule_id = "ACCEPTED_DATE_OVER_UMBRAL" THEN 2
WHEN rule_id = "ACCEPTED_DATE_LESS_UMBRAL" THEN 2
WHEN rule_id = "REGEX_VALID_DATE_1" THEN 2
WHEN rule_id = "REGEX_VALID_UPPER_STRING" THEN 2
WHEN rule_id = "VALUE_EQUAL_SUM_OTHER_COLUMNS" THEN 2
WHEN rule_id = "ACCEPTED_DATE_CUSTOM_RANGE" THEN 2
WHEN rule_id = "AVAILABLE_DAILY_DATE" THEN 2
END action
,CASE

WHEN rule_id = "NOT_NULL_SIMPLE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "NOT_BLANK" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "DISTINCT_VALUES" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_GROUP_FIX" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUES_ALWAYS_EXPECTED" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_COUNTRY_FIX" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "OUTOFRANGE_VS_VARIATION_OF_SAME_DAY_LW" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_2" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "Z_SCORE_OUTLIER_DETECT_NOTSUN_NOTHOL_LAST7D" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_POSITIVE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_ZERO_OR_POSITIVE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_BETWEEN_FIX_UMBRAL" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_BETWEEN_MOBILE_UMBRAL" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_LESS_OTHER_COLUMN" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "BIREADER_EQUAL_VALUES_OF_PAST_WEEKS_IN_CURRENT_WEEK" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "NO_REFERENTIAL_INTEGRITY_VIOLATION" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "NO_DUPLICATES_IN_COLUMN_GROUPS" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_DATE_FORMAT" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_DATE_RANGE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_DATE_OVER_UMBRAL" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_DATE_LESS_UMBRAL" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "REGEX_VALID_DATE_1" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "REGEX_VALID_UPPER_STRING" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "VALUE_EQUAL_SUM_OTHER_COLUMNS" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "ACCEPTED_DATE_CUSTOM_RANGE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
WHEN rule_id = "AVAILABLE_DAILY_DATE" THEN CONCAT("Hay algún error en: ",table_id, " y en campo: ",column_id)
END message
FROM `conjuntopruebaceep.dq_summary`
WHERE failed_count > 0;