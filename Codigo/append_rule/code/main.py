import functions_framework
import gspread
import os
from google.auth import default

@functions_framework.http
def append_rule(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://dataquality-genai.web.app",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "https://dataquality-genai.web.app"}

    request_data = request.get_json()
    result = insert_rule(request_data)

    return (result, 200, headers)

def insert_rule(data):
    
    dimension = data["DIMENSION"]
    cod = data["COD"]
    nombre_regla_yml = data["NOMBRE_REGLA_YML"]
    nombre_regla = data["NOMBRE_REGLA"]
    descripcion = data["DESCRIPCION"]
    ejemplo = data["EJEMPLO"]
    campo = data["CAMPO"]
    parametros = data["PARAMETROS"]
    severidad = data["SEVERIDAD"]
    accion1 = data["ACCION"]
    accion2 = data["ACCION_YML"]
    tipo_regla_yml = data["TIPO_REGLA_YML"]

    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials, _ = default(scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get("MATRIX_INPUT"))
    sheet = spreadsheet.worksheet('Reglas')

    valor_buscado = dimension

    filas = sheet.get_all_values()
    fila_a_insertar = None
    ok = False

    for i, fila in enumerate(filas):
        if fila[0].upper() == valor_buscado.upper():
            ok = True
        elif fila[0] is not None and ok and fila[0].strip() != "":
            fila_a_insertar = i
            break

    valores_nueva_fila = [dimension, cod, nombre_regla_yml, nombre_regla, descripcion, ejemplo, campo, parametros, severidad, accion1, accion2, tipo_regla_yml]
    sheet.insert_row(valores_nueva_fila, fila_a_insertar)

    print("Se ha insertado una nueva fila.")

    return {"rule_appended": "True"}
