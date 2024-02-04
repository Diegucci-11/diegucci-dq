import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
import gspread
import datetime
import base64
import smtplib
import os
import json
from email.message import EmailMessage
import re
import functions_framework

@functions_framework.http
def qae_notification(request):

    json_data = request.get_json()
    print("------------------------------------------")
    print(request)
    print("------------------------------------------")
    print(json_data)
    print("------------------------------------------")

    # data_json = json.loads(data)
    # men_error = (data_json['errorStatus']['message']).replace('\r','')
    # mensaje = men_error.split('&&&')
    # json_data = [1, 2, 3, 2, 3, 1, 2]
    severidad = json_data['data']

    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client = gspread.authorize(credentials)
    
    spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
    correos = spreadsheet.worksheet('Correos')
    tablas = spreadsheet.worksheet('Tablas')
    product = tablas.cell(2, 2).value
    env = tablas.cell(3, 2).value

    df_correos = pd.DataFrame(correos.get('A:D'))
    df_correos.dropna(how='all', axis=0, inplace=True)
    df_correos = df_correos.sort_values(by=df_correos.columns[3], ascending=False)
    correos_utilizados = []
    i = 0
    print(df_correos)
    for indice_fila, fila in df_correos.iloc[1:].iterrows():
        if fila[1] != '' and fila[1] is not None:
            if fila[1] not in correos_utilizados and (int(fila[3][0:1]) in severidad) and fila[2] == env:
                print("Entro en segundo if")
                enviarCorreo(fila[0], fila[1], fila[2], fila[3], product)
                correos_utilizados.append(fila[1])
    return ""

def enviarCorreo(name, email, env, severity, product):
    print("Entra en función enviarCorreo")
    with open('template.html', 'r') as file:
        body_template = file.read()

    body = body_template.format(nombre=name, producto=product, entorno=env, severidad=severity)
    gmail_user = "diegucci.sautter@gmail.com"
     
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(gmail_user, "jevy iqnh lljn kldh")
        print("Loggeo correcto en gmail")
        try:
            msg = EmailMessage()
            msg.set_content(body, subtype="html")
            msg['Subject'] = "ERRORES EN LA EJECUCIÓN DE LA ÚLTIMA TAREA"
            msg['From'] = gmail_user
            msg['To'] = email
            msg['Cc'] = ''
            msg['Bcc'] = ''
            smtp.send_message(msg)
            smtp.close()
            print("Mensaje enviado correctamente")
        except:
            print("Error en el envio del correo!")

# def recogerCorreos():
#     SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#     credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
#     client = gspread.authorize(credentials)

#     spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
#     correos = spreadsheet.worksheet('Correos')

#     df = pd.DataFrame()
#     df_correos = pd.DataFrame(correos.get('A:D'))

#     for indice_fila, fila in enumerate(correos.get_all_values()):
#         if fila[1] != '' and fila[1] is not None:
#             df[indice_fila] = fila
 
#     dataFrame = df.T
#     dataFrame.columns = dataFrame.iloc[0]
#     dataFrame = dataFrame.iloc[1:]
#     dataFrame['severidad'] = dataFrame['severidad'][0:1]
#     return dataFrame

# def productoEntorno(data):
#     lista = []
#     patronProducto = r"Producto: (\w+)"
#     patronEntorno = r"Entorno: (\w+)"
#     producto = re.search(patronProducto, data)
#     entorno = re.search(patronEntorno, data)
#     if(producto is not None and entorno is not None):
#         nombre_producto = producto.group(1)
#         lista.append(nombre_producto)
#         nombre_entorno = entorno.group(1)
#         lista.append(nombre_entorno)
#     return lista;

# def recogerSeveridad(data):
#     dic = data
#     query = dic.get("errorStatus").get("message")
#     lista = []
#     for i, letras in enumerate(query):
#         if letras == "\n":
#             lista.append(query[i+1:i+2])
#     return lista
