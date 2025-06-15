import os
import pandas as pd
import requests
from urllib.parse import urlencode
import re

# -------------------------------------------- FUNCIONES ------------------------------------------------------ #

def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        print("Archivo eliminado con éxito.")
    else:
        print("El archivo no existe.")

# --------------------------------------------------------------------------------------------------------------- #   

def extract_info_api(url, username, password):
    limit = 10000
    params = urlencode({"$limit": limit})
    url_read = f"{url}?{params}"
    response = requests.get(url_read, auth=(username, password))

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print("Error en la solicitud a la API:", response.status_code)

# --------------------------------------------------------------------------------------------------------------- #

def extract_full_url(text):
    match = re.search(r'https?://[^\'\s]+', text)
    if match:
        return match.group(0)
    else:
        return None

# --------------------------------------------------------------------------------------------------------------- #

def extract_url(text):
    match = re.search(r'https?://[^\s]+isFromPublicArea=True&isModal=true&asPopupView=true', text)
    if match:
        return match.group(0)
    else:
        return None

# --------------------------------------------------------------------------------------------------------------- #

def extract_twonumbers_after_dot(text):
    pattern = r"\.(\d{2})"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    return None

# --------------------------------------------------------------------------------------------------------------- #

def extract_fournumbers_after_dot(text):
    pattern = r"\.(\d{4})"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    return None

# --------------------------------------------------------------------------------------------------------------- #

def extract_sixnumbers_after_dot(text):
    pattern = r"\.(\d{6})"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    return None

# --------------------------------------------------------------------------------------------------------------- #

def extract_first_two_numbers(text):
    return text[:2]

# --------------------------------------------------------------------------------------------------------------- #

def generate_alert(df, today):
    
    for index in df.index:
        if df.loc[index, 'FECHA DE FIN DEL CONTRATO'] > today:
            df.loc[index, 'VERIFICACIÓN FINALIZACIÓN DEL CONTRATO'] = "No finalizado"
            df.loc[index, 'ESTADO CIERRE CPS'] = "Contrato CPS No finalizado"
            df.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO']= "Contrato No finalizado"
            df.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO'] = (df.loc[index, 'FECHA DE FIN DEL CONTRATO'] - today).days
            if df.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO']<30:
            df.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Menos de 1 mes para finalizar"
            elif 30 <= df.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO'] <= 60:
            df.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Entre 1 y 2 meses para finalizar"
            else:
            df.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Más de 2 meses para finalizar"
        else:
            df.loc[index, 'VERIFICACIÓN FINALIZACIÓN DEL CONTRATO'] = "Finalizado"
            if df.loc[index, 'ESTADO CONTRATO'] in (['Modificado','En ejecución','Suspendido','Activo','cedido']):
            if df.loc[index,'ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']==True:
                df.loc[index, 'ESTADO CIERRE CPS'] = "No cerrado"
                df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = (today - df.loc[index, 'FECHA DE FIN DEL CONTRATO']).days
                if df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR']>1095:
                df.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Más de 3 años sin cerrar"
                elif 730 <= df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] <= 1095:
                df.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Entre 2 y 3 años sin cerrar"
                else:
                df.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Menos de 2 años sin cerrar"
            else:

                df.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO'] = "No liquidado"
                df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR'] = (today - df.loc[index, 'FECHA DE FIN DEL CONTRATO']).days
                if df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR']>1095:
                df.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Más de 3 años sin liquidar"
                elif 730 <= df.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR'] <= 1095:
                df.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Entre 2 y 3 años sin liquidar"
                else:
                df.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Menos de 2 años sin liquidar"
    return df

# --------------------------------------------------------------------------------------------------------------- #

def generate_contract_management(df):
    for index in df.index:
        if df.loc[index,'ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']==True:
            df.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO'] = "El contrato no se liquida"
        else:
            df.loc[index, 'ESTADO CIERRE CPS'] = "El contrato debe liquidarse"
    return df

# --------------------------------------------------------------------------------------------------------------- #