import functions_framework
import json
import vertexai
from vertexai.language_models import CodeChatModel
from google.cloud import bigquery
from google.auth import default

BQ_DATASET = "dq_v2_rule_dictionary"
BQ_TABLE = "rule_dictionary"

@functions_framework.http
def rule_generator(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://dataquality-genai.web.app",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "https://tfg-generador-de-reglas.web.app/"}

    request_data = request.get_json()
    result = create_rule(request_data)

    return (result, 200, headers)


def create_rule(data):
    test_prompt = data["prompt"]
    dimension = data["dimension"]

    vertexai.init(project="tfg-dq", location="europe-west3")
    chat_model = CodeChatModel.from_pretrained("codechat-bison")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2
    }
    chat = chat_model.start_chat()

    datos_entrenamiento = cargar_datos_entrenamiento()
    sublists = [datos_entrenamiento[i:i+10] for i in range(0, len(datos_entrenamiento), 10)]

    for sublist in sublists:
        list_string = str(sublist)
        chat.send_message(list_string, **parameters)
    
    rule = chat.send_message("A partir de esos ejemplos que te mandé, necesito que me crees otra regla de calidad con todos esos campos y mismo formato a partir de este prompt:\n" + test_prompt + "\nY con esta dimensión: " + dimension + "\nNO MUESTRES NADA MÁS QUE NO SEA EL CÓDIGO JSON", **parameters)
    rule = rule.text
    rule = rule[8:-3]

    rule_json = json.dumps(rule)

    return rule_json

def cargar_datos_entrenamiento():
    SCOPES = ["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/drive"]
    credentials, _ = default(scopes=SCOPES)
    client = bigquery.Client(credentials=credentials)

    sql_query = f"""
            SELECT *
            FROM {BQ_DATASET}.{BQ_TABLE}
        """

    query_job = client.query(sql_query)
    results = [dict(row) for row in query_job]
    return results
