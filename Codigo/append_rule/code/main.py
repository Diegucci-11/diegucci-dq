import functions_framework
import gspread
import os
from google.auth import default
import json

@functions_framework.http
def append_rule(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://tfg-generador-de-reglas.web.app",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "https://tfg-generador-de-reglas.web.app"}

    # request_data = request.get_json()
    raw_body = request.get_data(as_text=True)
    request_data = json.loads(raw_body)
    result = insert_rule(request_data)

    return (result, 200, headers)

def insert_rule(data):
    dimension = data["DIMENSION"]
    nombre_regla_yml = data["NOMBRE_REGLA_YML"]
    descripcion = data["DESCRIPCION"]
    ejemplo = data["EJEMPLO"]
    tipo_dato = data["TIPO_DATO"]
    parametros = data["PARAMETROS"]
    severidad = data["SEVERIDAD"]
    accion = data["ACCION"]
    codigo = data["CODIGO_YML"]
    tipo_regla_yml = data["TIPO_REGLA_YML"]

    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials, _ = default(scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get("MATRIX_FILE"))
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

    valores_nueva_fila = [dimension, nombre_regla_yml, descripcion, ejemplo, tipo_dato, parametros, severidad, accion, codigo, tipo_regla_yml]
    sheet.insert_row(valores_nueva_fila, fila_a_insertar)

    print("Se ha insertado una nueva fila.")

    return {"rule_appended": "True"}
