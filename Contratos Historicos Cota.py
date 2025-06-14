import pandas as pd
import numpy as np
from openpyxl import load_workbook
import re
import requests
import json
from urllib.parse import urlencode
from datetime import date, datetime

today = date.today()

base_url_CONTRATOS_SECOPII = 'https://www.datos.gov.co/resource/nmbi-zvgs.json'

username = 'druizf01@gmail.com'
password = 'Chocorramo33*'

limit = 1000000
params = urlencode({'$limit': limit})
url = f'{base_url_CONTRATOS_SECOPII}?{params}'

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    data = response.json()
    df_CONTRATOS_SECOPII = pd.DataFrame(data)
else:
    print('Error en la solicitud a la API:', response.status_code)

df_CONTRATOS_SECOPII.shape

df_CONTRATOS_SECOPII.columns

reemplazos_columnas_CONTRATOS_SECOPII = {
    'nombre_entidad': 'Nombre Entidad',
    'nit_entidad': 'Nit Entidad',
    'departamento': 'Departamento',
    'ciudad': 'Ciudad',
    'localizaci_n': 'Localización',
    'orden': 'Orden',
    'sector': 'Sector',
    'rama': 'Rama',
    'entidad_centralizada': 'Entidad Centralizada',
    'proceso_de_compra': 'Proceso de Compra',
    'id_contrato': 'ID Contrato',
    'referencia_del_contrato': 'Referencia del Contrato',
    'estado_contrato': 'Estado Contrato',
    'codigo_de_categoria_principal': 'Codigo de Categoria Principal',
    'descripcion_del_proceso': 'Descripcion del Proceso',
    'tipo_de_contrato': 'Tipo de Contrato',
    'modalidad_de_contratacion': 'Modalidad de Contratacion',
    'justificacion_modalidad_de': 'Justificacion Modalidad de Contratacion',
    'fecha_de_firma': 'Fecha de Firma',
    'fecha_de_inicio_del_contrato': 'Fecha de Inicio del Contrato',
    'fecha_de_fin_del_contrato': 'Fecha de Fin del Contrato',
    'fecha_de_inicio_de_ejecucion': 'Fecha de Inicio de Ejecucion',
    'fecha_de_fin_de_ejecucion': 'Fecha de Fin de Ejecucion',
    'condiciones_de_entrega': 'Condiciones de Entrega',
    'tipodocproveedor': 'TipoDocProveedor',
    'documento_proveedor': 'Documento Proveedor',
    'proveedor_adjudicado': 'Proveedor Adjudicado',
    'es_grupo': 'Es Grupo',
    'es_pyme': 'Es Pyme',
    'habilita_pago_adelantado': 'Habilita Pago Adelantado',
    'liquidaci_n': 'Liquidación',
    'obligaci_n_ambiental': 'Obligación Ambiental',
    'obligaciones_postconsumo': 'Obligaciones Postconsumo',
    'reversion': 'Reversion',
    'origen_de_los_recursos': 'Origen de los Recursos',
    'destino_gasto': 'Destino Gasto',
    'valor_del_contrato': 'Valor del Contrato',
    'valor_de_pago_adelantado': 'Valor de pago adelantado',
    'valor_facturado': 'Valor Facturado',
    'valor_pendiente_de_pago': 'Valor Pendiente de Pago',
    'valor_pagado': 'Valor Pagado',
    'valor_amortizado': 'Valor Amortizado',
    'valor_pendiente_de': 'Valor Pendiente de Amortizacion',
    'valor_pendiente_de_ejecucion': 'Valor Pendiente de Ejecucion',
    'estado_bpin': 'Estado BPIN',
    'c_digo_bpin': 'Código BPIN',
    'anno_bpin': 'Anno BPIN',
    'saldo_cdp': 'Saldo CDP',
    'saldo_vigencia': 'Saldo Vigencia',
    'espostconflicto': 'EsPostConflicto',
    'dias_adicionados': 'Dias adicionados',
    'puntos_del_acuerdo': 'Puntos del Acuerdo',
    'pilares_del_acuerdo': 'Pilares del Acuerdo',
    'urlproceso': 'URLProceso',
    'nombre_representante_legal': 'Nombre Representante Legal',
    'nacionalidad_representante_legal': 'Nacionalidad Representante Legal',
    'domicilio_representante_legal': 'Domicilio Representante Legal',
    'tipo_de_identificaci_n_representante_legal': 'Tipo de Identificación Representante Legal',
    'identificaci_n_representante_legal': 'Identificación Representante Legal',
    'g_nero_representante_legal': 'Género Representante Legal',
    'presupuesto_general_de_la_nacion_pgn': 'Presupuesto General de la Nacion – PGN',
    'sistema_general_de_participaciones': 'Sistema General de Participaciones',
    'sistema_general_de_regal_as': 'Sistema General de Regalías',
    'recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_': 'Recursos Propios (Alcaldías, Gobernaciones y Resguardos Indígenas)',
    'recursos_de_credito': 'Recursos de Credito',
    'recursos_propios': 'Recursos Propios',
    'ultima_actualizacion': 'Ultima Actualizacion',
    'codigo_entidad': 'Codigo Entidad',
    'codigo_proveedor': 'Codigo Proveedor',
    'fecha_inicio_liquidacion': 'Fecha Inicio Liquidacion',
    'fecha_fin_liquidacion': 'Fecha Fin Liquidacion',
    'objeto_del_contrato': 'Objeto del Contrato'
}

df_CONTRATOS_SECOPII.rename(columns=reemplazos_columnas_CONTRATOS_SECOPII, inplace=True)

df_CONTRATOS_SECOPII.columns

cols=list(df_CONTRATOS_SECOPII.columns)
cols=[x.upper().strip() for x in cols]
df_CONTRATOS_SECOPII.columns=cols

df_CONTRATOS_SECOPII.columns

#df_CONTRATOS_SECOPII.drop(columns='ANNO BPIN',inplace=True)

df_CONTRATOS_SECOPII.head(5)

print(f"Tamaño del set antes de eliminar contratos repetidos: {df_CONTRATOS_SECOPII.shape} ")
df_CONTRATOS_SECOPII.drop_duplicates(subset='REFERENCIA DEL CONTRATO', inplace=True)
print(f"Tamaño del set después de eliminar contratos repetidos: {df_CONTRATOS_SECOPII.shape}")

df_CONTRATOS_SECOPII['ESTADO CONTRATO'].unique()

print(f"Tamaño del set antes de eliminar los estados: {df_CONTRATOS_SECOPII.shape} ")
df_CONTRATOS_SECOPII = df_CONTRATOS_SECOPII[df_CONTRATOS_SECOPII['ESTADO CONTRATO'].isin(['En ejecución', 'Modificado', 'cedido', 'terminado','Cerrado','Activo','Prorrogado','Suspendido'])]
print(f"Tamaño del set después de eliminar los estados: {df_CONTRATOS_SECOPII.shape}")

df_CONTRATOS_SECOPII['CODIGO DE CATEGORIA PRINCIPAL'] = df_CONTRATOS_SECOPII['CODIGO DE CATEGORIA PRINCIPAL'].astype(str)

def extract_numbers_segmento(text):
    match = re.search(r'V1\.(\d{2})', text)
    if match:
        return match.group(1)
    else:
        return ''

def extract_numbers_familia(text):
    match = re.search(r'V1\.(\d{4})', text)
    if match:
        return match.group(1)
    else:
        return ''


def extract_numbers_clase(text):
    match = re.search(r'V1\.(\d{6})', text)
    if match:
        return match.group(1)
    else:
        return ''

df_CONTRATOS_SECOPII.loc[:,'SEGMENTO'] = df_CONTRATOS_SECOPII['CODIGO DE CATEGORIA PRINCIPAL'].apply(extract_numbers_segmento)
df_CONTRATOS_SECOPII.loc[:,'FAMILIA'] = df_CONTRATOS_SECOPII['CODIGO DE CATEGORIA PRINCIPAL'].apply(extract_numbers_familia)
df_CONTRATOS_SECOPII.loc[:,'CLASE'] = df_CONTRATOS_SECOPII['CODIGO DE CATEGORIA PRINCIPAL'].apply(extract_numbers_clase)

print(df_CONTRATOS_SECOPII['SEGMENTO'].unique())
print(df_CONTRATOS_SECOPII['FAMILIA'].unique())
print(df_CONTRATOS_SECOPII['CLASE'].unique())

tipos_de_datos_CONTRATOS_SECOPII = df_CONTRATOS_SECOPII.dtypes

tipos_de_datos_CONTRATOS_SECOPII


columnas_fecha = ['FECHA DE FIRMA', 'FECHA DE INICIO DEL CONTRATO', 'FECHA DE FIN DEL CONTRATO']


print("Formatos de fecha iniciales:")
for columna in columnas_fecha:
    print(f'{columna}: {df_CONTRATOS_SECOPII[columna].dtype}')


df_CONTRATOS_SECOPII[columnas_fecha] = df_CONTRATOS_SECOPII[columnas_fecha].apply(pd.to_datetime)


print("\nFormatos de fecha después del cambio:")
for columna in columnas_fecha:
    print(f'{columna}: {df_CONTRATOS_SECOPII[columna].dtype}')

df_CONTRATOS_SECOPII['FECHA DE FIRMA'].fillna(df_CONTRATOS_SECOPII['FECHA DE INICIO DEL CONTRATO'], inplace=True)


df_CONTRATOS_SECOPII['VALOR DEL CONTRATO'] = pd.to_numeric(df_CONTRATOS_SECOPII['VALOR DEL CONTRATO'], errors='coerce').astype(float)

df_CONTRATOS_SECOPII['NOMBRE ENTIDAD'].unique()

reemplazos_nombre_entidad = {'ALCALDÍA MUNICIPAL COTA':'ALCALDÍA DE COTA',
                             'CUNDINAMARCA - ALCALDIA MUNICIPIO DE COTA':'ALCALDÍA DE COTA',
                             'ALCALDIA DE COTA':'ALCALDÍA DE COTA',
                             'INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA CUNDINAMARCA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE COTA':'IMRD',
                             'EMPRESA DE SERVICIOS PUBLICOS DE COTA SA ESP':'EMSERCOTA',
                             'CUNDINAMARCA - EMSERCOTA S.A. E.S.P. - COTA':'EMSERCOTA',
                             }

df_CONTRATOS_SECOPII.loc[:,'DEPENDENCIA'] = df_CONTRATOS_SECOPII['NOMBRE ENTIDAD'].replace(reemplazos_nombre_entidad)

df_CONTRATOS_SECOPII['DEPENDENCIA'].unique()

df_CONTRATOS_SECOPII['MODALIDAD DE CONTRATACION'].unique()

reemplazos_modalidad = {
    'Contratación Directa (con ofertas)': 'Contratación Directa', 'Contratación directa':'Contratación Directa',
    'Contratación Directa (Ley 1150 de 2007)':'Contratación Directa','No Definido':'Contratación Directa',
    'Contratación Directa Menor Cuantía':'Contratación Directa',
    'Contratación Mínima Cuantía':'Mínima Cuantía',
    'Selección abreviada subasta inversa': 'Selección Abreviada', 'Selección Abreviada de Menor Cuantía': 'Selección Abreviada',
    'Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes': 'Selección Abreviada',
    'Selección Abreviada de Menor Cuantía (Ley 1150 de 2007)':'Selección Abreviada',
    'Subasta':'Selección Abreviada','Selección Abreviada servicios de Salud':'Selección Abreviada',
    'Contratación régimen especial (con ofertas)':'Régimen especial',
    'Licitación pública Obra Publica':'Licitación Pública','Licitación Pública Acuerdo Marco de Precios':'Licitación Pública',
    'Licitación obra pública':'Licitación Pública',
    'Contratos y convenios con más de dos partes':'Convenios','Concurso de Méritos con Lista Corta':'Concurso de Méritos',
    'CCE-20-Concurso_Meritos_Sin_Lista_Corta_1Sobre':'Concurso de Méritos', 'Concurso de méritos abierto':'Concurso de Méritos',
    'CCE-19-Concurso_Meritos_Con_Lista_Corta_1Sobre':'Concurso de Méritos','Concurso de Méritos Abierto':'Concurso de Méritos',
    'Solicitud de información a los Proveedores':'RFI','CONTRATACION DIRECTA (LEY 1150 DE 2007)': 'Contratación Directa',
    'CONTRATACION MINIMA CUANTIA':'Mínima Cuantía', 'CONCURSO DE MERITOS ABIERTO':'Concurso de Méritos',
    'REGIMEN ESPECIAL':'Régimen especial', 'SUBASTA':'Selección Abreviada', 'LICITACION PUBLICA':'Licitación Pública',
    'SELECCION ABREVIADA DE MENOR CUANTIA (LEY 1150 DE 2007)':'Selección Abreviada',
    'LICITACION OBRA PUBLICA':'Licitación Pública',
    'CONTRATOS Y CONVENIOS CON MAS DE DOS PARTES':'Convenios',
    'CONTRATACION DIRECTA MENOR CUANTIA': 'Contratación Directa',
    'CONCURSO DE MERITOS CON LISTA CORTA':'Concurso de Méritos',
    'SELECCION ABREVIADA SERVICIOS DE SALUD':'Selección Abreviada'
}

df_CONTRATOS_SECOPII.loc[:,'MODALIDAD GENERAL'] = df_CONTRATOS_SECOPII['MODALIDAD DE CONTRATACION'].replace(reemplazos_modalidad)

df_CONTRATOS_SECOPII['MODALIDAD GENERAL'].unique()

df_CONTRATOS_SECOPII['JUSTIFICACION MODALIDAD DE CONTRATACION'].unique()

reemplazos_justificacion_modalidad = {
    'Prestación de Servicios Profesionales y de Apoyo a la Gestión (Literal H)': 'Servicios Profesionales',
    'ServiciosProfesionales': 'Servicios Profesionales',
    'Contratos para el Desarrollo de Actividades Científicas y Tecnológicas (Literal E)': 'Servicios Profesionales',
    'PrestamoDeUso': 'Préstamo de uso',
    'Urgencia Manifiesta (Literal A)': 'Urgencia manifiesta',
    'Contratos Interadministrativos (Literal C)': 'Contratos/Convenios Interadministrativos',
    'ContratosConveniosInteradministrativosValorCero': 'Contratos/Convenios Interadministrativos',
    'PluralityContractsDevelopment': 'Servicios Profesionales',
    'Arrendamiento o Adquisición de Inmuebles (Literal I)': 'Arrendamiento de inmuebles',
    'Presupuesto inferior al 10% de la menor cuantía': 'Presupuesto menor al 10% de la Menor Cuantía',
    'Ley 1150 de 2007': 'Ley 1150 de 2007',
    'PluralityPrestacion': 'Servicios Profesionales',
    'Presupuesto menor al 10% de la Menor Cuantía': 'Presupuesto menor al 10% de la Menor Cuantía',
    'Suministro de bienes y servicios de características técnicas uniformes y común utilización': 'B/S características técnicas uniformes',
    'Cuando no Exista Pluralidad de Oferentes en el Mercado (Literal G)': 'No pluralidad de oferentes en el mercado',
    'No existe pluralidad de oferentes en el mercado': 'No pluralidad de oferentes en el mercado',
    'AcquisitionOfPropertyOther': 'Otro (financiación)',
    'ContratacionDeEmprestitos': 'Crédito Público/Empréstito',
    'Decree092/2017': 'Decreto 092/2017',
    'Article30_1993': 'Ley 1150 de 2007',
    'ContratosConveniosInteradministrativosConValor': 'Contratos/Convenios Interadministrativos',
    'PluralityContractingServices': 'Servicios Profesionales',
    'Proceso de licitación pública declarado desierto': 'Proceso de licitación pública declarado desierto',
    'Servicios profesionales y apoyo a la gestión': 'Servicios Profesionales',
    'Operaciones de Crédito Público': 'Crédito Público/Empréstito',
    'Contratación de Empréstitos (Literal B)': 'Crédito Público/Empréstito',
    'Contratos para el desarrollo de actividades científicas y tecnológicas': 'Actividades científicas y tecnológicas',
    'Contratos o convenios Interadministrativos (valor cero)': 'Contratos/Convenios Interadministrativos',
    'Contratos o convenios Interadministrativos (con valor)': 'Contratos/Convenios Interadministrativos',
    'Prestamo de uso': 'Préstamo de uso',
    'Contratos de bienes y servicios sujetos a reserva': 'B/S sujetos a reserva',
    'Adquisición de inmuebles': 'Adquisición de inmuebles',
    'Contratación de Bienes y Servicios en el Sector Defensa y en el DAS (Literal D)': 'Bienes y Servicios Sector Defensa',
    'Contratos de Encargo Fiduciario que Celebren Entidades Territoriales (Literal F)': 'Encargo Fiduciario',
    'PRESTACION DE SERVICIOS PROFESIONALES Y DE APOYO A LA GESTION (LITERAL H)': 'Servicios Profesionales',
    'ARRENDAMIENTO O ADQUISICION DE INMUEBLES (LITERAL I)': 'Arrendamiento de inmuebles',
    'CONTRATOS DE ENCARGO FIDUCIARIO QUE CELEBREN ENTIDADES TERRITORIALES (LITERAL F)': 'Encargo Fiduciario',
    'CONTRATOS INTERADMINISTRATIVOS (LITERAL C)': 'Contratos/Convenios Interadministrativos',
    'CUANDO NO EXISTA PLURALIDAD DE OFERENTES EN EL MERCADO (LITERAL G)': 'No pluralidad de oferentes en el mercado',
    'No Definido': 'No Definido por la Entidad',
    'CONTRATACION DE EMPRESTITOS (LITERAL B)': 'Crédito Público/Empréstito',
    'CONTRATACION DE BIENES Y SERVICIOS EN EL SECTOR DEFENSA Y EN EL DAS (LITERAL D)': 'Bienes y Servicios Sector Defensa',
    'URGENCIA MANIFIESTA (LITERAL A)': 'Urgencia manifiesta',
    'CONTRATOS PARA EL DESARROLLO DE ACTIVIDADES CIENTIFICAS Y TECNOLOGICAS (LITERAL E)': 'Actividades científicas y tecnológicas'
}


df_CONTRATOS_SECOPII.loc[:,'JUSTIFICACIÓN MODALIDAD GENERAL']=df_CONTRATOS_SECOPII['JUSTIFICACION MODALIDAD DE CONTRATACION'].replace(reemplazos_justificacion_modalidad)

df_CONTRATOS_SECOPII['JUSTIFICACIÓN MODALIDAD GENERAL'].unique()

df_CONTRATOS_SECOPII_credito_publico = df_CONTRATOS_SECOPII[df_CONTRATOS_SECOPII['JUSTIFICACIÓN MODALIDAD GENERAL'].isin(['Crédito Público/Empréstito'])]

df_CONTRATOS_SECOPII = df_CONTRATOS_SECOPII[df_CONTRATOS_SECOPII['JUSTIFICACIÓN MODALIDAD GENERAL'] != 'Crédito Público/Empréstito']

df_CONTRATOS_SECOPII['TIPO DE CONTRATO'].unique()

reemplazos_tipos_de_contrato = {
    'Servicios de aprovisionamiento': 'S. de aprovisionamiento',
    'Alquiler de edificios': 'Alquiler de edificios',
    'Suministros': 'Suministros',
    'Compraventa': 'Compraventa',
    'Interventoría': 'Interventoría',
    '27 - Otros servicios': 'Otros servicios',
    'Decreto 092 de 2017': 'Decreto 092 de 2017',
    'Seguros': 'Servicios financieros',
    'Arrendamiento Muebles': 'Arrendamiento',
    'Obra': 'Obra',
    'Concesión': 'Concesión',
    'Otro Tipo de Contrato': 'Otros servicios',
    'Prestación de Servicios': 'Prestación de Servicios',
    'Consultoría': 'Consultoría',
    'Arrendamiento': 'Arrendamiento',
    'Comodato': 'Comodato',
    'Otro': 'Otros servicios',
    'DecreeLaw092/2017': 'Decreto 092 de 2017',
    'No Especificado': 'Prestación de Servicios',
    'Arrendamiento de muebles': 'Arrendamiento',
    'Emprestito': 'Crédito Público/Empréstito',
    'Arrendamiento de inmuebles': 'Arrendamiento',
    'Servicios financieros': 'Servicios financieros',
    'S. de aprovisionamiento': 'S. de aprovisionamiento',
    'Prestación de servicios': 'Prestación de Servicios',
    'Operaciones de Crédito Público': 'Crédito Público/Empréstito',
    'ND': 'Crédito Público/Empréstito',
    'PRESTACION DE SERVICIOS': 'Prestación de Servicios',
    'ARRENDAMIENTO': 'Arrendamiento',
    'INTERVENTORIA': 'Interventoría',
    'COMPRAVENTA': 'Compraventa',
    'OTRO TIPO DE CONTRATO': 'Otros servicios',
    'COMODATO': 'Comodato',
    'SUMINISTRO': 'Suministros',
    'OBRA': 'Obra',
    'CONSULTORIA': 'Consultoría',
    'CREDITO': 'Crédito Público/Empréstito',
    'CONCESION': 'Concesión'
}

df_CONTRATOS_SECOPII.loc[:,'TIPO DE CONTRATO GENERAL']=df_CONTRATOS_SECOPII['TIPO DE CONTRATO'].replace(reemplazos_tipos_de_contrato)

df_CONTRATOS_SECOPII['TIPO DE CONTRATO GENERAL'].unique()

df_CONTRATOS_SECOPII.loc[:,'ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']=(df_CONTRATOS_SECOPII['TIPO DE CONTRATO GENERAL'].isin(['Prestación de Servicios']) & df_CONTRATOS_SECOPII['MODALIDAD GENERAL'].isin(['Contratación Directa']))

df_CONTRATOS_SECOPII['ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']

today1 = datetime.combine(date.today(), datetime.min.time())

for index in df_CONTRATOS_SECOPII.index:
    if df_CONTRATOS_SECOPII.loc[index, 'FECHA DE FIN DEL CONTRATO'] > today1:
        df_CONTRATOS_SECOPII.loc[index, 'VERIFICACIÓN FINALIZACIÓN DEL CONTRATO'] = "No finalizado"
        df_CONTRATOS_SECOPII.loc[index, 'ESTADO CIERRE CPS'] = "Contrato CPS No finalizado"
        df_CONTRATOS_SECOPII.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO']= "Contrato No finalizado"
        df_CONTRATOS_SECOPII.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO'] = (df_CONTRATOS_SECOPII.loc[index, 'FECHA DE FIN DEL CONTRATO'] - today1).days
        if df_CONTRATOS_SECOPII.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO']<30:
          df_CONTRATOS_SECOPII.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Menos de 1 mes para finalizar"
        elif 30 <= df_CONTRATOS_SECOPII.loc[index, 'DÍAS PARA LA FINALIZACIÓN DEL CONTRATO'] <= 60:
          df_CONTRATOS_SECOPII.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Entre 1 y 2 meses para finalizar"
        else:
          df_CONTRATOS_SECOPII.loc[index, 'ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'] = "Más de 2 meses para finalizar"
    else:
        df_CONTRATOS_SECOPII.loc[index, 'VERIFICACIÓN FINALIZACIÓN DEL CONTRATO'] = "Finalizado"
        if df_CONTRATOS_SECOPII.loc[index, 'ESTADO CONTRATO'] in (['Modificado','En ejecución','Suspendido','Activo','cedido']):
          if df_CONTRATOS_SECOPII.loc[index,'ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']==True:
            df_CONTRATOS_SECOPII.loc[index, 'ESTADO CIERRE CPS'] = "No cerrado"
            df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = (today1 - df_CONTRATOS_SECOPII.loc[index, 'FECHA DE FIN DEL CONTRATO']).days
            if df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR']>1095:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Más de 3 años sin cerrar"
            elif 730 <= df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] <= 1095:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Entre 2 y 3 años sin cerrar"
            else:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'] = "Menos de 2 años sin cerrar"
          else:

            df_CONTRATOS_SECOPII.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO'] = "No liquidado"
            df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR'] = (today1 - df_CONTRATOS_SECOPII.loc[index, 'FECHA DE FIN DEL CONTRATO']).days
            if df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR']>1095:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Más de 3 años sin liquidar"
            elif 730 <= df_CONTRATOS_SECOPII.loc[index, 'DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR'] <= 1095:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Entre 2 y 3 años sin liquidar"
            else:
              df_CONTRATOS_SECOPII.loc[index, 'ALERTA CONTRATO SIN LIQUIDAR'] = "Menos de 2 años sin liquidar"

df_CONTRATOS_SECOPII['ESTADO CIERRE CPS'].fillna("Cerrado",inplace=True)

df_CONTRATOS_SECOPII['ESTADO LIQUIDACIÓN CONTRATO'].fillna("Liquidado",inplace=True)

for index in df_CONTRATOS_SECOPII.index:
  if df_CONTRATOS_SECOPII.loc[index,'ES CONTRATO DE PRESTACIÓN DE SERVICIOS MODALIDAD DIRECTA']==True:
    df_CONTRATOS_SECOPII.loc[index, 'ESTADO LIQUIDACIÓN CONTRATO'] = "El contrato no se liquida"
  else:
    df_CONTRATOS_SECOPII.loc[index, 'ESTADO CIERRE CPS'] = "El contrato debe liquidarse"

df_CONTRATOS_SECOPII['ESTADO CIERRE CPS'].unique()

df_CONTRATOS_SECOPII['ESTADO LIQUIDACIÓN CONTRATO'].unique()

df_CONTRATOS_SECOPII['VERIFICACIÓN FINALIZACIÓN DEL CONTRATO'].unique()

df_CONTRATOS_SECOPII['DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'].unique()

df_CONTRATOS_SECOPII['DÍAS DESDE LA FINALIZACIÓN DEL CONTRATO SIN LIQUIDAR'].unique()

df_CONTRATOS_SECOPII['DÍAS PARA LA FINALIZACIÓN DEL CONTRATO'].unique()

df_CONTRATOS_SECOPII['ALERTA CONTRATO SIN LIQUIDAR'].unique()

df_CONTRATOS_SECOPII['ALERTA CONTRATO DE PRESTACIÓN DE SERVICIOS SIN CERRAR'].unique()

df_CONTRATOS_SECOPII['ALERTA PARA LA FINALIZACIÓN DEL CONTRATO'].unique()



df_CONTRATOS_SECOPII.loc[:, 'URLPROCESO'] = df_CONTRATOS_SECOPII['URLPROCESO'].astype(str)

def extract_full_url(text):
    match = re.search(r'https?://[^\'\s]+', text)
    if match:
        return match.group(0)
    else:
        return None


df_CONTRATOS_SECOPII.loc[:, 'ENLACE DEL PROCESO'] = df_CONTRATOS_SECOPII['URLPROCESO'].apply(extract_full_url)

df_CONTRATOS_SECOPII['ENLACE DEL PROCESO'].head()

df_CONTRATOS_SECOPII.loc[:,'PLATAFORMA']="SECOP II"

df_CONTRATOS_SECOPII.columns























base_url_CONTRATOS_SECOPI = 'https://www.datos.gov.co/resource/8ebu-adji.json'

limit = 1000000
params = urlencode({'$limit': limit})
url = f'{base_url_CONTRATOS_SECOPI}?{params}'

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    data = response.json()
    df_CONTRATOS_SECOPI = pd.DataFrame(data)
else:
    print('Error en la solicitud a la API:', response.status_code)

df_CONTRATOS_SECOPI.shape

df_CONTRATOS_SECOPI.columns

reemplazos_columnas_CONTRATOS_SECOPI = {
    'uid': 'UID',
    'anno_cargue_secop': 'Anno Cargue SECOP',
    'anno_firma_contrato': 'Anno Firma Contrato',
    'nivel_entidad': 'Nivel Entidad',
    'orden_entidad': 'Orden Entidad',
    'nombre_entidad': 'Nombre Entidad',
    'nit_de_la_entidad': 'NIT de la Entidad',
    'c_digo_de_la_entidad': 'Código de la Entidad',
    'id_modalidad': 'ID Modalidad',
    'modalidad_de_contratacion': 'Modalidad de Contratacion',
    'estado_del_proceso': 'Estado del Proceso',
    'causal_de_otras_formas_de': 'Causal de Otras formas de Contratacion Directa',
    'id_regimen_de_contratacion': 'ID Regimen de Contratacion',
    'nombre_regimen_de_contratacion': 'Nombre Regimen de Contratacion',
    'id_objeto_a_contratar': 'ID Objeto a Contratar',
    'objeto_a_contratar': 'Objeto a Contratar',
    'detalle_del_objeto_a_contratar': 'Detalle del Objeto a Contratar',
    'tipo_de_contrato': 'Tipo De Contrato',
    'municipio_de_obtencion': 'Municipio de Obtencion',
    'municipio_de_entrega': 'Municipio de Entrega',
    'municipios_ejecucion': 'Municipios Ejecucion',
    'fecha_de_cargue_en_el_secop': 'Fecha de Cargue en el SECOP',
    'numero_de_constancia': 'Numero de Constancia',
    'numero_de_proceso': 'Numero de Proceso',
    'numero_de_contrato': 'Numero de Contrato',
    'cuantia_proceso': 'Cuantia Proceso',
    'id_grupo': 'ID Grupo',
    'nombre_grupo': 'Nombre Grupo',
    'id_familia': 'ID Familia',
    'nombre_familia': 'Nombre Familia',
    'id_clase': 'ID Clase',
    'nombre_clase': 'Nombre Clase',
    'id_adjudicacion': 'ID Adjudicacion',
    'tipo_identifi_del_contratista': 'Tipo Identifi del Contratista',
    'identificacion_del_contratista': 'Identificacion del Contratista',
    'nom_razon_social_contratista': 'Nom Razon Social Contratista',
    'dpto_y_muni_contratista': 'Dpto y Muni Contratista',
    'tipo_doc_representante_legal': 'Tipo Doc Representante Legal',
    'identific_representante_legal': 'Identific Representante Legal',
    'nombre_del_represen_legal': 'Nombre del Represen Legal',
    'fecha_de_firma_del_contrato': 'Fecha de Firma del Contrato',
    'fecha_ini_ejec_contrato': 'Fecha Ini Ejec Contrato',
    'plazo_de_ejec_del_contrato': 'Plazo de Ejec del Contrato',
    'rango_de_ejec_del_contrato': 'Rango de Ejec del Contrato',
    'tiempo_adiciones_en_dias': 'Tiempo Adiciones en Dias',
    'tiempo_adiciones_en_meses': 'Tiempo Adiciones en Meses',
    'fecha_fin_ejec_contrato': 'Fecha Fin Ejec Contrato',
    'compromiso_presupuestal': 'Compromiso Presupuestal',
    'cuantia_contrato': 'Cuantia Contrato',
    'valor_total_de_adiciones': 'Valor Total de Adiciones',
    'valor_contrato_con_adiciones': 'Valor Contrato con Adiciones',
    'objeto_del_contrato_a_la': 'Objeto del Contrato a la Firma',
    'proponentes_seleccionados': 'Proponentes Seleccionados',
    'calificacion_definitiva': 'Calificacion Definitiva',
    'id_sub_unidad_ejecutora': 'ID Sub Unidad Ejecutora',
    'nombre_sub_unidad_ejecutora': 'Nombre Sub Unidad Ejecutora',
    'ruta_proceso_en_secop_i': 'Ruta Proceso en SECOP I',
    'moneda': 'Moneda',
    'es_postconflicto': 'Es PostConflicto',
    'marcacion_adiciones': 'Marcacion Adiciones',
    'posicion_rubro': 'Posicion Rubro',
    'nombre_rubro': 'Nombre Rubro',
    'valor_rubro': 'Valor Rubro',
    'sexo_replegal': 'Sexo RepLegal',
    'pilar_acuerdo_paz': 'Pilar Acuerdo Paz',
    'punto_acuerdo_paz': 'Punto Acuerdo Paz',
    'municipio_entidad': 'Municipio Entidad',
    'departamento_entidad': 'Departamento Entidad',
    'ultima_actualizacion': 'Ultima Actualizacion',
    'fecha_liquidacion': 'Fecha Liquidacion',
    'cumpledecreto248': 'Cumple Decreto 248',
    'incluyebienesdecreto248': 'Incluye Bienes Decreto 248'
}

df_CONTRATOS_SECOPI.rename(columns=reemplazos_columnas_CONTRATOS_SECOPI, inplace=True)

df_CONTRATOS_SECOPI.columns

cols=list(df_CONTRATOS_SECOPI.columns)
cols=[x.upper().strip() for x in cols]
df_CONTRATOS_SECOPI.columns=cols

df_CONTRATOS_SECOPI.columns

df_CONTRATOS_SECOPI.head()

df_CONTRATOS_SECOPI['NUMERO DE CONTRATO']

print(f"Tamaño del set antes de eliminar contratos repetidos: {df_CONTRATOS_SECOPI.shape} ")
df_CONTRATOS_SECOPI.drop_duplicates(subset='NUMERO DE CONTRATO', inplace=True)
print(f"Tamaño del set después de eliminar contratos repetidos: {df_CONTRATOS_SECOPI.shape}")

df_CONTRATOS_SECOPI['ESTADO DEL PROCESO'].unique()

Reemplazos_estados_secopi={'CELEBRADO':'Celebrado', 'LIQUIDADO':'Liquidado', 'TERMINADO SIN LIQUIDAR':'Terminado sin Liquidar',
'CONVOCADO':'Convocado', 'ADJUDICADO':'Adjudicado', 'LISTA CORTA':'Lista Corta','INVITACIÓN ABIERTA':'Invitación Abierta','EXPRESIÓN DE INTERÉS':'Expresión de Interés',
'LISTA MULTIUSOS':'Lista Multiusos','INVITACIÓN CERRADA': 'Invitación Cerrada'
}

df_CONTRATOS_SECOPI.loc[:,'ESTADO DEL PROCESO']=df_CONTRATOS_SECOPI['ESTADO DEL PROCESO'].replace(Reemplazos_estados_secopi)

df_CONTRATOS_SECOPI['ESTADO DEL PROCESO'].unique()

print(f"Tamaño del set antes de eliminar los estados: {df_CONTRATOS_SECOPI.shape} ")
df_CONTRATOS_SECOPI = df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['ESTADO DEL PROCESO'].isin(['Liquidado', 'Celebrado', 'Terminado sin Liquidar', 'CONVOCADO', 'ADJUDICADO', 'LISTA CORTA','INVITACIÓN ABIERTA','EXPRESIÓN DE INTERÉS', 'LISTA MULTIUSOS','INVITACIÓN CERRADA'])]
print(f"Tamaño del set después de eliminar los estados: {df_CONTRATOS_SECOPI.shape}")

print(f"Tamaño del set antes de eliminar los NO DEFINIDOS: {df_CONTRATOS_SECOPI.shape} ")
df_CONTRATOS_SECOPI = df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['NOM RAZON SOCIAL CONTRATISTA'] != 'No Definido']
print(f"Tamaño del set después de eliminar los NO DEFINIDOS: {df_CONTRATOS_SECOPI.shape}")

df_CONTRATOS_SECOPI['NOMBRE ENTIDAD'].unique()

df_CONTRATOS_SECOPI = df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['NOMBRE ENTIDAD'] != 'CUNDINAMARCA - PERSONERIA MUNICIPAL DE COTA']

df_CONTRATOS_SECOPI['NOMBRE ENTIDAD'].unique()

df_CONTRATOS_SECOPI.loc[:,'DEPENDENCIA'] = df_CONTRATOS_SECOPI['NOMBRE ENTIDAD'].replace(reemplazos_nombre_entidad)

df_CONTRATOS_SECOPI['DEPENDENCIA'].unique()

df_CONTRATOS_SECOPI['MODALIDAD DE CONTRATACION'].unique()

df_CONTRATOS_SECOPI.loc[:,'MODALIDAD GENERAL'] = df_CONTRATOS_SECOPI['MODALIDAD DE CONTRATACION'].replace(reemplazos_modalidad)

df_CONTRATOS_SECOPI['MODALIDAD GENERAL'].unique()

df_CONTRATOS_SECOPI['CAUSAL DE OTRAS FORMAS DE CONTRATACION DIRECTA'].unique()

df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['CAUSAL DE OTRAS FORMAS DE CONTRATACION DIRECTA'].isin(['No Definido'])].shape

df_CONTRATOS_SECOPI.loc[:,'JUSTIFICACIÓN MODALIDAD GENERAL']=df_CONTRATOS_SECOPI['CAUSAL DE OTRAS FORMAS DE CONTRATACION DIRECTA'].replace(reemplazos_justificacion_modalidad)

df_CONTRATOS_SECOPI['JUSTIFICACIÓN MODALIDAD GENERAL'].unique()

df_CONTRATOS_SECOPI.shape

df_CONTRATOS_SECOPI_credito_publico = df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['JUSTIFICACIÓN MODALIDAD GENERAL'].isin(['Crédito Público/Empréstito'])]

df_CONTRATOS_SECOPI = df_CONTRATOS_SECOPI[df_CONTRATOS_SECOPI['JUSTIFICACIÓN MODALIDAD GENERAL'] != 'Crédito Público/Empréstito']

df_CONTRATOS_SECOPI.shape

df_CONTRATOS_SECOPI['TIPO DE CONTRATO'].unique()

df_CONTRATOS_SECOPI.loc[:,'TIPO DE CONTRATO GENERAL']=df_CONTRATOS_SECOPI['TIPO DE CONTRATO'].replace(reemplazos_tipos_de_contrato)

df_CONTRATOS_SECOPI['TIPO DE CONTRATO GENERAL'].unique()

df_CONTRATOS_SECOPI['ID CLASE'].unique()

df_CONTRATOS_SECOPI['ID FAMILIA'].unique()

df_CONTRATOS_SECOPI.loc[:,'ID SEGMENTO'] = df_CONTRATOS_SECOPI['ID FAMILIA'].astype(str).str[:2]

df_CONTRATOS_SECOPI['ID SEGMENTO'].unique()

# Reemplazar los valores de 'ID CLASE', 'ID SEGMENTO' y 'ID FAMILIA' con vacíos si 'ID CLASE' es 'No definido'
mask = df_CONTRATOS_SECOPI['ID CLASE'] == 'No definido'
df_CONTRATOS_SECOPI.loc[mask, ['ID CLASE', 'ID SEGMENTO', 'ID FAMILIA']] = ''

df_CONTRATOS_SECOPI['ID SEGMENTO'].unique()

df_CONTRATOS_SECOPI.dtypes

df_CONTRATOS_SECOPI['FECHA DE FIRMA DEL CONTRATO']

columnas_fecha = ['FECHA DE FIRMA DEL CONTRATO', 'FECHA INI EJEC CONTRATO', 'FECHA FIN EJEC CONTRATO','FECHA DE CARGUE EN EL SECOP']


print("Formatos de fecha iniciales:")
for columna in columnas_fecha:
    print(f'{columna}: {df_CONTRATOS_SECOPI[columna].dtype}')


for columna in columnas_fecha:
    df_CONTRATOS_SECOPI[columna] = pd.to_datetime(df_CONTRATOS_SECOPI[columna])
#, format='%d/%m/%Y', errors='coerce'

print("\nFormatos de fecha después del cambio:")
for columna in columnas_fecha:
    print(f'{columna}: {df_CONTRATOS_SECOPI[columna].dtype}')

df_CONTRATOS_SECOPI['FECHA DE FIRMA DEL CONTRATO']

df_CONTRATOS_SECOPI['FECHA DE FIRMA DEL CONTRATO'].fillna(df_CONTRATOS_SECOPI['FECHA DE CARGUE EN EL SECOP'], inplace=True)

df_CONTRATOS_SECOPI.loc[:,'CUANTIA CONTRATO'] = pd.to_numeric(df_CONTRATOS_SECOPI['CUANTIA CONTRATO'], errors='coerce').astype(float)

df_CONTRATOS_SECOPI.loc[:,'PLATAFORMA']="SECOP I"

df_CONTRATOS_SECOPI['RUTA PROCESO EN SECOP I']

df_CONTRATOS_SECOPI.loc[:, 'RUTA PROCESO EN SECOP I'] = df_CONTRATOS_SECOPI['RUTA PROCESO EN SECOP I'].astype(str)
df_CONTRATOS_SECOPI.loc[:, 'ENLACE DEL PROCESO'] = df_CONTRATOS_SECOPI['RUTA PROCESO EN SECOP I'].apply(extract_full_url)

df_CONTRATOS_SECOPI['ENLACE DEL PROCESO'].unique()



base_url = 'https://www.datos.gov.co/resource/g8ap-7zzf.json'

limit = 20000

params = urlencode({'$limit': limit})
url = f'{base_url}?{params}'

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    data = response.json()
    df_CONTRATOS_TVEC = pd.DataFrame(data)
else:
    print('Error en la solicitud a la API:', response.status_code)

df_CONTRATOS_TVEC.columns

reemplazos_columnas_TVEC = {
    'a_o': 'Año',
    'identificador_de_la_orden': 'Identificador de la Orden',
    'agregacion': 'Agregacion',
    'rama_de_la_entidad': 'Rama de la Entidad',
    'sector_de_la_entidad': 'Sector de la Entidad',
    'entidad': 'Entidad',
    'orden_de_la_entidad': 'Orden de la Entidad',
    'nit_entidad': 'NIT Entidad',
    'solicitante': 'Solicitante',
    'fecha': 'Fecha',
    'proveedor': 'Proveedor',
    'estado': 'Estado',
    'solicitud': 'Solicitud',
    'items': 'Items',
    'total': 'Total',
    'ciudad': 'Ciudad',
    'entidad_obigada': 'Entidad Obigada',
    'espostconflicto': 'EsPostconflicto',
    'nit_proveedor': 'NIT proveedor',
    'actividad_economica_proveedor': 'Actividad Economica Proveedor'
}

df_CONTRATOS_TVEC.rename(columns=reemplazos_columnas_TVEC, inplace=True)

df_CONTRATOS_TVEC.columns

cols=list(df_CONTRATOS_TVEC.columns)
cols=[x.upper().strip() for x in cols]
df_CONTRATOS_TVEC.columns=cols

df_CONTRATOS_TVEC.columns

print(f'Tamaño del set antes de eliminar las OC Repetidas: {df_CONTRATOS_TVEC.shape} ')
df_CONTRATOS_TVEC.drop_duplicates(subset='IDENTIFICADOR DE LA ORDEN', keep='first', inplace=True)
print(f'Tamaño del set después de eliminar las OC Repetidas: {df_CONTRATOS_TVEC.shape}')

df_CONTRATOS_TVEC['IDENTIFICADOR DE LA ORDEN'].unique()

print(df_CONTRATOS_TVEC['FECHA'].dtype)
df_CONTRATOS_TVEC['FECHA'] = pd.to_datetime(df_CONTRATOS_TVEC['FECHA'], errors='coerce')
print(df_CONTRATOS_TVEC['FECHA'].dtype)

print(df_CONTRATOS_TVEC['TOTAL'].dtype)
df_CONTRATOS_TVEC['TOTAL'] = pd.to_numeric(df_CONTRATOS_TVEC['TOTAL'], errors='coerce')
print(df_CONTRATOS_TVEC['TOTAL'].dtype)

df_CONTRATOS_TVEC['ENTIDAD'].unique()

df_CONTRATOS_TVEC=df_CONTRATOS_TVEC[df_CONTRATOS_TVEC['ENTIDAD'].isin(['ALCALDIA DE COTA','CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE COTA'])]

df_CONTRATOS_TVEC['ENTIDAD'].unique()

df_CONTRATOS_TVEC.loc[:,'DEPENDENCIA'] = df_CONTRATOS_TVEC['ENTIDAD'].replace(reemplazos_nombre_entidad)

df_CONTRATOS_TVEC['DEPENDENCIA'].unique()

df_CONTRATOS_TVEC['AGREGACION'].unique()

reemplazos_agregacion_general={
    'GRANDES SUPERFICIES': 'Grandes Superficies',
    'TRANSPORTE TERRESTRES ESPECIAL DE PASAJEROS II': 'Transporte Terrestre Especial de Pasajeros II',
    'DOTACION ESCOLAR II': 'Dotación Escolar II',
    'ASEO Y CAFETERIA III': 'Aseo y Cafetería III',
    'MOTOCICLETAS, CUATRIMOTOS Y MOTOCARROS II': 'Motocicletas Cuatrimotos y Motocarros II',
    'VEHICULOS I': 'Vehículos I',
    'COMBUSTIBLE (BOGOTA) II': 'Combustible (Bogotá) II',
    'VEHICULOS III': 'Vehículos III',
    'ETP III': 'ETP III',
    'CONSUMIBLES DE IMPRESION II': 'Consumibles de Impresión II',
    'COMPRA DE ETP II': 'ETP II'
}

df_CONTRATOS_TVEC.loc[:,'AGREGACION GENERAL'] = df_CONTRATOS_TVEC['AGREGACION'].replace(reemplazos_agregacion_general)


df_CONTRATOS_TVEC['AGREGACION GENERAL'].unique()

reemplazos_id_clase={
    'Grandes Superficies': '561115',
    'Transporte Terrestre Especial de Pasajeros II': '781118',
    'Dotación Escolar II': '561120',
    'Aseo y Cafetería III': '761115',
    'Motocicletas Cuatrimotos y Motocarros II': '251018',
    'Vehículos I': '251015',
    'Combustible (Bogotá) II': '151015',
    'Vehículos III': '251015',
    'ETP III': '432115',
    'Consumibles de Impresión II': '441031',
    'ETP II': '432115',
    'ASEO Y CAFETERIA IV': '761115',
    'MATERIALES DE CONSTRUCCION Y FERRETERIA': '311628',
       'ATENCION A EMERGENCIAS':'461915'
}

df_CONTRATOS_TVEC.loc[:,'ID CLASE'] = df_CONTRATOS_TVEC['AGREGACION GENERAL'].replace(reemplazos_id_clase)

df_CONTRATOS_TVEC['ID CLASE'].unique()

df_CONTRATOS_TVEC.loc[:,'ID SEGMENTO'] = df_CONTRATOS_TVEC['ID CLASE'].astype(str).str[:2]
df_CONTRATOS_TVEC.loc[:,'ID FAMILIA'] = df_CONTRATOS_TVEC['ID CLASE'].astype(str).str[:4]

df_CONTRATOS_TVEC['ID SEGMENTO'].unique()

df_CONTRATOS_TVEC['ID FAMILIA'].unique()

df_CONTRATOS_TVEC.loc[:,'TIPO DE CONTRATO GENERAL']='Orden de Compra - TVEC'
df_CONTRATOS_TVEC.loc[:,'MODALIDAD GENERAL']='IAD - Acuerdo Marco'
df_CONTRATOS_TVEC.loc[:,'JUSTIFICACIÓN MODALIDAD GENERAL']='B. y S. de características técnicas uniformes'

df_CONTRATOS_TVEC.loc[:,'ENLACE DEL PROCESO'] = 'https://www.colombiacompra.gov.co/tienda-virtual-del-estado-colombiano/ordenes-compra/' + df_CONTRATOS_TVEC['IDENTIFICADOR DE LA ORDEN'].astype(str)

df_CONTRATOS_TVEC['ENLACE DEL PROCESO'].unique()

df_CONTRATOS_TVEC.loc[:,'PLATAFORMA']="TVEC"

df_CONTRATOS_TVEC.columns

df_CONTRATOS_TVEC.loc[:,'NIT PROVEEDOR']="No diligenciado"

#df_CONTRATOS_SECOPI_integrar_vigencias=df_CONTRATOS_SECOPI[['NUMERO DE CONTRATO','FECHA INI EJEC CONTRATO','FECHA FIN EJEC CONTRATO',
#                                                            'ESTADO DEL PROCESO','NIT DE LA ENTIDAD', 'DEPENDENCIA' , 'DETALLE DEL OBJETO A CONTRATAR',
#                                                            'ID SEGMENTO','ID FAMILIA','ID CLASE', 'TIPO DE CONTRATO GENERAL', 'MODALIDAD GENERAL',
#                                                            'JUSTIFICACIÓN MODALIDAD GENERAL','FECHA DE FIRMA DEL CONTRATO', 'IDENTIFICACION DEL CONTRATISTA',
#                                                            'NOM RAZON SOCIAL CONTRATISTA', 'CUANTIA CONTRATO', 'ENLACE DEL PROCESO','PLATAFORMA']]

#df_CONTRATOS_SECOPII_integrar_vigencias=df_CONTRATOS_SECOPII[['REFERENCIA DEL CONTRATO','FECHA DE INICIO DEL CONTRATO','FECHA DE FIN DEL CONTRATO',
#                                                              'ESTADO CONTRATO','NIT ENTIDAD','DEPENDENCIA', 'DESCRIPCION DEL PROCESO',
#                                                              'SEGMENTO','FAMILIA','CLASE','TIPO DE CONTRATO GENERAL', 'MODALIDAD GENERAL',
#                                                              'JUSTIFICACIÓN MODALIDAD GENERAL','FECHA DE FIRMA','DOCUMENTO PROVEEDOR', 'PROVEEDOR ADJUDICADO',
#                                                              'VALOR DEL CONTRATO','ENLACE DEL PROCESO','PLATAFORMA']]

df_CONTRATOS_SECOPII.drop('ANNO BPIN',inplace=True,axis=1)

df_CONTRATOS_SECOPI=df_CONTRATOS_SECOPI.reset_index().drop('index', axis=1)
df_CONTRATOS_SECOPII=df_CONTRATOS_SECOPII.reset_index().drop('index', axis=1)
df_CONTRATOS_TVEC=df_CONTRATOS_TVEC.reset_index().drop('index', axis=1)

df_CONTRATOS_SECOPI_integrar=df_CONTRATOS_SECOPI[['NUMERO DE CONTRATO','ESTADO DEL PROCESO','DEPENDENCIA' , 'DETALLE DEL OBJETO A CONTRATAR',
                                                  'ID SEGMENTO','ID FAMILIA','ID CLASE',
                                                  'TIPO DE CONTRATO GENERAL', 'MODALIDAD GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','FECHA DE FIRMA DEL CONTRATO',
                                                  'IDENTIFICACION DEL CONTRATISTA', 'NOM RAZON SOCIAL CONTRATISTA', 'CUANTIA CONTRATO', 'ENLACE DEL PROCESO','PLATAFORMA']]

df_CONTRATOS_SECOPII_integrar=df_CONTRATOS_SECOPII[['REFERENCIA DEL CONTRATO','ESTADO CONTRATO','DEPENDENCIA', 'DESCRIPCION DEL PROCESO',
                                                    'SEGMENTO','FAMILIA','CLASE',
                                                    'TIPO DE CONTRATO GENERAL', 'MODALIDAD GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','FECHA DE FIRMA',
                                                    'DOCUMENTO PROVEEDOR', 'PROVEEDOR ADJUDICADO','VALOR DEL CONTRATO','ENLACE DEL PROCESO','PLATAFORMA']]

df_CONTRATOS_TVEC_integrar=df_CONTRATOS_TVEC[['IDENTIFICADOR DE LA ORDEN','ESTADO','DEPENDENCIA', 'AGREGACION GENERAL',
                                              'ID SEGMENTO','ID FAMILIA','ID CLASE',
                                              'TIPO DE CONTRATO GENERAL', 'MODALIDAD GENERAL',
                                              'JUSTIFICACIÓN MODALIDAD GENERAL','FECHA',
                                              'NIT PROVEEDOR', 'PROVEEDOR', 'TOTAL','ENLACE DEL PROCESO','PLATAFORMA']]

columnas=df_CONTRATOS_SECOPII_integrar.columns
df_CONTRATOS_SECOPI_integrar.columns=columnas
df_CONTRATOS_TVEC_integrar.columns=columnas

INTEGRADO = pd.concat([df_CONTRATOS_SECOPI_integrar, df_CONTRATOS_SECOPII_integrar,df_CONTRATOS_TVEC_integrar])

INTEGRADO.loc[:,'HOY'] = today
#INTEGRADO['HOY'] = pd.to_datetime(INTEGRADO['HOY'])

INTEGRADO['HOY']

today

dataframes = {'Sheet1': INTEGRADO, 'S1': df_CONTRATOS_SECOPI, 'S2': df_CONTRATOS_SECOPII,'TVEC':df_CONTRATOS_TVEC}

with pd.ExcelWriter('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/INTEGRADO.xlsx') as writer:
    for sheet_name, df in dataframes.items():
        df.to_excel(writer, sheet_name=sheet_name, index=True)

print("Archivo Excel creado con éxito.")

#INTEGRADO.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/INTEGRADO.xlsx')
