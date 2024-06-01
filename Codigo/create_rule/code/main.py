import functions_framework
import json
import vertexai
from vertexai.language_models import CodeChatModel
from google.auth import default
import gspread

@functions_framework.http
def create_rule(request):

    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://tfg-generador-de-reglas.web.app",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "https://tfg-generador-de-reglas.web.app"}

    raw_body = request.get_data(as_text=True)
    request_data = json.loads(raw_body)

    result = generate_rule(request_data)
    
    return (result, 200, headers)


def generate_rule(data):
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
    print(rule)
    return json.dumps(rule.replace("'", "\""))

def cargar_datos_entrenamiento():
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials, _ = default(scopes=SCOPES)

    client = gspread.authorize(credentials)
    spreadsheet = client.open("Matrix_Input_v2")
    reglas_sheet = spreadsheet.worksheet('Reglas')

    cell_values = reglas_sheet.get_all_values()
    data = [dict(zip(cell_values[1], row)) for row in cell_values[2:]]
    return data

