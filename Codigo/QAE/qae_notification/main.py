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

@functions_framework.cloud_event
def qae_notification(cloud_event):

    data = (base64.b64decode(cloud_event.data["message"]["data"])).decode('utf-8')
    data_json = json.loads(data)
    men_error = (data_json['errorStatus']['message']).replace('\r','')
    mensaje = men_error.split('&&&')
    listaSeveridad = recogerSeveridad(data_json)
    listado = productoEntorno(data)
    correos = recogerCorreos()

    dicEmailTo = {}
    for i in range(0, len(correos)):
        if (correos.iloc[i][2].lower() == listado[1].lower()  and correos.iloc[i][3] in listaSeveridad):
            if correos.iloc[i][1] not in dicEmailTo:
                dicEmailTo[correos.iloc[i][1]] = [correos.iloc[i][3]]
            else:
                print(correos.iloc[i][1] + " " + correos.iloc[i][1])
                lista = dicEmailTo.get(correos.iloc[i][1])
                lista.append(correos.iloc[i][3]) 
                dicEmailTo[correos.iloc[i][1]] = lista

    for emailTo in dicEmailTo:
        severidades = dicEmailTo[emailTo]
        enviarCorreo(emailTo, mensaje, listado,severidades)

def enviarCorreo(emailTo, mensaje, listado, severidades):
    with open('template.html', 'r') as file:
        body_template = file.read()

    nombre = 'Data Quality'
    identificacion = ' '
    errores = mensaje[0]
    link = 'www.google.es'
    severity = ""
    if(len(severidades) == 1):
        for a in severidades:
            severity += " " + a
    else:
        severity += " " + str(severidades[0])
        for a in severidades[1:]:
            severity += ", " + str(a)
            
    body = body_template.format(nombre=nombre, identificacion=identificacion, errores=errores, link=link, 
                                producto=listado[0], entorno=listado[1], severidad=severity)
    gmail_user = "diegucci.sautter@gmail.com"
    # gmail_password = get_gmail_password("clave")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(gmail_user, gmail_password)
        try:
            msg = EmailMessage()
            msg.set_content(body, subtype="html")
            msg['Subject'] = "ERRORES EN LA EJECUCIÓN DE LA ÚLTIMA TAREA"
            msg['From'] = gmail_user
            msg['To'] = emailTo
            msg['Cc'] = ''
            msg['Bcc'] = ''
            smtp.send_message(msg)
            smtp.close()
        except:
            print("Error en el envio del correo!")

def recogerCorreos():
    SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('DQ_KEY')), scopes=SCOPES)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(os.environ.get('MATRIX_FILE'))
    correos = spreadsheet.worksheet('Correos')

    df = pd.DataFrame()
    df_correos = pd.DataFrame(correos.get('A:D'))

    for indice_fila, fila in enumerate(correos.get_all_values()):
        if fila[1] != '' and fila[1] is not None:
            df[indice_fila] = fila
 
    dataFrame = df.T
    dataFrame.columns = dataFrame.iloc[0]
    dataFrame = dataFrame.iloc[1:]
    dataFrame['severidad'] = dataFrame['severidad'][0:1]
    return dataFrame

def productoEntorno(data):
    lista = []
    patronProducto = r"Producto: (\w+)"
    patronEntorno = r"Entorno: (\w+)"
    producto = re.search(patronProducto, data)
    entorno = re.search(patronEntorno, data)
    if(producto is not None and entorno is not None):
        nombre_producto = producto.group(1)
        lista.append(nombre_producto)
        nombre_entorno = entorno.group(1)
        lista.append(nombre_entorno)
    return lista;

def recogerSeveridad(data):
    dic = data
    query = dic.get("errorStatus").get("message")
    lista = []
    for i, letras in enumerate(query):
        if letras == "\n":
            lista.append(query[i+1:i+2])
    return lista
