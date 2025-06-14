#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from openpyxl import load_workbook
import re
import requests
import json
from urllib.parse import urlencode
from datetime import date


# In[3]:


CONTRATOS2024_SECOPII_PATH='/content/drive/MyDrive/Colab Notebooks/Proyectos personales/INTEGRADO.xlsx'


# In[4]:


df_contratos_s2=pd.read_excel(CONTRATOS2024_SECOPII_PATH,sheet_name='S2')


# In[5]:


df_contratos_s2_2024=df_contratos_s2[df_contratos_s2['FECHA DE FIRMA'].dt.year ==2024]


# In[6]:


df_contratos_s2_2024.shape


# In[7]:


base_url_PROCESOS_SECOPII = 'https://www.datos.gov.co/resource/naza-xjvd.json'


# In[8]:


username = 'druizf01@gmail.com'
password = 'Chocorramo33*'


# In[9]:


limit = 1000000
params = urlencode({'$limit': limit})
url = f'{base_url_PROCESOS_SECOPII}?{params}'


# In[10]:


response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    data = response.json()
    df_PROCESOS_SECOP_II = pd.DataFrame(data)
else:
    print('Error en la solicitud a la API:', response.status_code)


# In[11]:


df_PROCESOS_SECOP_II.shape


# In[12]:


reemplazos_columnas_PROCESOS_SECOPII = {
    'entidad': 'Entidad',
    'nit_entidad': 'Nit Entidad',
    'departamento_entidad': 'Departamento Entidad',
    'ciudad_entidad': 'Ciudad Entidad',
    'ordenentidad': 'OrdenEntidad',
    'codigo_pci': 'Entidad Centralizada',
    'id_del_proceso': 'ID del Proceso',
    'referencia_del_proceso': 'Referencia del Proceso',
    'ppi': 'PCI',
    'id_del_portafolio': 'ID del Portafolio',
    'nombre_del_procedimiento': 'Nombre del Procedimiento',
    'descripci_n_del_procedimiento': 'Descripción del Procedimiento',
    'fase': 'Fase',
    'fecha_de_publicacion_del': 'Fecha de Publicacion del Proceso',
    'fecha_de_ultima_publicaci': 'Fecha de Ultima Publicación',
    'fecha_de_publicacion_fase': 'Fecha de Publicacion (Fase Planeacion Precalificacion)',
    'fecha_de_publicacion_fase_1': 'Fecha de Publicacion (Fase Seleccion Precalificacion)',
    'fecha_de_publicacion': 'Fecha de Publicacion (Manifestacion de Interes)',
    'fecha_de_publicacion_fase_2': 'Fecha de Publicacion (Fase Borrador)',
    'fecha_de_publicacion_fase_3': 'Fecha de Publicacion (Fase Seleccion)',
    'precio_base': 'Precio Base',
    'modalidad_de_contratacion': 'Modalidad de Contratacion',
    'justificaci_n_modalidad_de': 'Justificación Modalidad de Contratación',
    'duracion': 'Duracion',
    'unidad_de_duracion': 'Unidad de Duracion',
    'fecha_de_recepcion_de': 'Fecha de Recepcion de Respuestas',
    'fecha_de_apertura_de_respuesta': 'Fecha de Apertura de Respuesta',
    'fecha_de_apertura_efectiva': 'Fecha de Apertura Efectiva',
    'ciudad_de_la_unidad_de': 'Ciudad de la Unidad de Contratación',
    'nombre_de_la_unidad_de': 'Nombre de la Unidad de Contratación',
    'proveedores_invitados': 'Proveedores Invitados',
    'proveedores_con_invitacion': 'Proveedores con Invitacion Directa',
    'visualizaciones_del': 'Visualizaciones del Procedimiento',
    'proveedores_que_manifestaron': 'Proveedores que Manifestaron Interes',
    'respuestas_al_procedimiento': 'Respuestas al Procedimiento',
    'respuestas_externas': 'Respuestas Externas',
    'conteo_de_respuestas_a_ofertas': 'Conteo de Respuestas a Ofertas',
    'proveedores_unicos_con': 'Proveedores Unicos con Respuestas',
    'numero_de_lotes': 'Numero de Lotes',
    'estado_del_procedimiento': 'Estado del Procedimiento',
    'id_estado_del_procedimiento': 'ID Estado del Procedimiento',
    'adjudicado': 'Adjudicado',
    'id_adjudicacion': 'ID Adjudicacion',
    'codigoproveedor': 'CodigoProveedor',
    'departamento_proveedor': 'Departamento Proveedor',
    'ciudad_proveedor': 'Ciudad Proveedor',
    'fecha_adjudicacion': 'Fecha Adjudicacion',
    'valor_total_adjudicacion': 'Valor Total Adjudicacion',
    'nombre_del_adjudicador': 'Nombre del Adjudicador',
    'nombre_del_proveedor': 'Nombre del Proveedor Adjudicado',
    'nit_del_proveedor_adjudicado': 'NIT del Proveedor Adjudicado',
    'codigo_principal_de_categoria': 'Codigo Principal de Categoria',
    'estado_de_apertura_del_proceso': 'Estado de Apertura del Proceso',
    'tipo_de_contrato': 'Tipo de Contrato',
    'subtipo_de_contrato': 'Subtipo de Contrato',
    'categorias_adicionales': 'Categorias Adicionales',
    'urlproceso': 'URLProceso',
    'codigo_entidad': 'Codigo Entidad',
    'estado_resumen': 'Estado Resumen'
}


# In[13]:


df_PROCESOS_SECOP_II.rename(columns=reemplazos_columnas_PROCESOS_SECOPII,inplace=True)


# In[14]:


df_PROCESOS_SECOP_II.columns


# In[15]:


cols=list(df_PROCESOS_SECOP_II.columns)
cols=[x.upper().strip() for x in cols]
df_PROCESOS_SECOP_II.columns=cols

df_PROCESOS_SECOP_II.columns


# In[16]:


columnas_fecha = ['FECHA DE PUBLICACION DEL PROCESO', 'FECHA DE ULTIMA PUBLICACIÓN', 'FECHA DE PUBLICACION (FASE SELECCION)']


print("Formatos de fecha iniciales:")
for columna in columnas_fecha:
    print(f'{columna}: {df_PROCESOS_SECOP_II[columna].dtype}')

df_PROCESOS_SECOP_II[columnas_fecha] = df_PROCESOS_SECOP_II[columnas_fecha].apply(pd.to_datetime)

print("\nFormatos de fecha después del cambio:")
for columna in columnas_fecha:
    print(f'{columna}: {df_PROCESOS_SECOP_II[columna].dtype}')


# In[17]:


df_publicacion=df_PROCESOS_SECOP_II.copy()


# In[18]:


df_PROCESOS_SECOP_II.sort_values(by ='FECHA DE PUBLICACION DEL PROCESO',ascending = False,inplace=True)


# In[19]:


print(f'Tamaño del set antes de definir la fecha de última publicación del estado actual de cada proceso: {df_PROCESOS_SECOP_II.shape} ')
df_PROCESOS_SECOP_II.drop_duplicates(subset='ID DEL PORTAFOLIO', keep='first', inplace=True)
print(f'Tamaño del set después de definir la fecha de última publicación del estado actual de cada proceso: {df_PROCESOS_SECOP_II.shape}')


# In[20]:


df_publicacion.sort_values(by ='FECHA DE PUBLICACION DEL PROCESO',ascending = True,inplace=True)


# In[21]:


print(f'Tamaño del set antes de definir la fecha de primera publicación del estado actual de cada proceso: {df_publicacion.shape} ')
df_publicacion.drop_duplicates(subset='ID DEL PORTAFOLIO', keep='first', inplace=True)
print(f'Tamaño del set después de definir la fecha de primera publicación del estado actual de cada proceso: {df_publicacion.shape}')


# In[22]:


df_publicacion.set_index('ID DEL PORTAFOLIO',inplace=True)


# In[23]:


df_PROCESOS_SECOP_II = pd.merge(df_PROCESOS_SECOP_II, df_publicacion['FECHA DE PUBLICACION DEL PROCESO'], left_on='ID DEL PORTAFOLIO', right_index=True, how='left')
df_PROCESOS_SECOP_II.shape


# In[24]:


df_PROCESOS_SECOP_II.rename(columns={'FECHA DE PUBLICACION DEL PROCESO_y': 'FECHA DE PUBLICACIÓN INICIAL','FECHA DE PUBLICACION DEL PROCESO_x': 'FECHA DE PUBLICACIÓN FINAL'}, inplace=True)


# In[25]:


df_PROCESOS_SECOP_II['FECHA DE PUBLICACIÓN INICIAL'].unique()


# In[26]:


df_PROCESOS_SECOP_II.shape


# In[27]:


df_PROCESOS_SECOP_II.shape


# In[28]:


cruce_id_proceso=df_contratos_s2_2024


# In[29]:


duplicados_df = df_PROCESOS_SECOP_II['ID DEL PORTAFOLIO'].duplicated().sum()
print(f"Número de filas duplicadas en la db de proceso 2024: {duplicados_df}")


# In[30]:


df_PROCESOS_SECOP_II= df_PROCESOS_SECOP_II.drop_duplicates(subset=['ID DEL PORTAFOLIO'])


# In[31]:


duplicados_cruce_id_proceso = cruce_id_proceso['PROCESO DE COMPRA'].duplicated().sum()
print(f"Número de filas duplicadas en cruce_id_proceso: {duplicados_cruce_id_proceso}")


# In[32]:


cruce_id_proceso= cruce_id_proceso.drop_duplicates(subset=['PROCESO DE COMPRA'])


# In[33]:


df_PROCESOS_SECOP_II = pd.merge(df_PROCESOS_SECOP_II, cruce_id_proceso[['FECHA DE FIRMA','FECHA DE INICIO DEL CONTRATO','VALOR DEL CONTRATO','DESTINO GASTO','ID CONTRATO', 'REFERENCIA DEL CONTRATO', 'ESTADO CONTRATO','DOCUMENTO PROVEEDOR', 'PROVEEDOR ADJUDICADO', 'ES GRUPO', 'ES PYME','PROCESO DE COMPRA','DEPENDENCIA','MODALIDAD GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','TIPO DE CONTRATO GENERAL']], left_on='ID DEL PORTAFOLIO', right_on='PROCESO DE COMPRA', how='left')


# In[34]:


df_PROCESOS_SECOP_II.shape


# In[35]:


df_PROCESOS_SECOP_II['DEPENDENCIA'].unique()


# In[36]:


reemplazos_nombre_entidad = {'ALCALDÍA MUNICIPAL COTA':'ALCALDÍA DE COTA',
                             'CUNDINAMARCA - ALCALDIA MUNICIPIO DE COTA':'ALCALDÍA DE COTA',
                             'ALCALDIA DE COTA':'ALCALDÍA DE COTA',
                             'INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA CUNDINAMARCA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE COTA':'IMRD',
                             'EMPRESA DE SERVICIOS PUBLICOS DE COTA SA ESP':'EMSERCOTA',
                             'CUNDINAMARCA - EMSERCOTA S.A. E.S.P. - COTA':'EMSERCOTA',
                             }


# In[37]:


df_PROCESOS_SECOP_II.loc[:,'DEPENDENCIA'] = df_PROCESOS_SECOP_II['ENTIDAD'].replace(reemplazos_nombre_entidad)
df_PROCESOS_SECOP_II['DEPENDENCIA'].unique()


# In[38]:


df_PROCESOS_SECOP_II['MODALIDAD GENERAL'].unique()


# In[39]:


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
    'Solicitud de información a los Proveedores':'RFI'
}


# In[40]:


df_PROCESOS_SECOP_II.loc[:,'MODALIDAD GENERAL'] = df_PROCESOS_SECOP_II['MODALIDAD DE CONTRATACION'].replace(reemplazos_modalidad)
df_PROCESOS_SECOP_II['MODALIDAD GENERAL'].unique()


# In[41]:


df_PROCESOS_SECOP_II['JUSTIFICACIÓN MODALIDAD GENERAL'].unique()


# In[42]:


reemplazos_justificacion_modalidad = {'Prestación de Servicios Profesionales y de Apoyo a la Gestión (Literal H)':'Servicios Profesionales',
    'ServiciosProfesionales': 'Servicios Profesionales','Contratos para el Desarrollo de Actividades Científicas y Tecnológicas (Literal E)': 'Servicios Profesionales',
    'PrestamoDeUso': 'Préstamo de uso',
    'Urgencia Manifiesta (Literal A)': 'Urgencia manifiesta','Contratos Interadministrativos (Literal C)':'Contratos/Convenios Interadministrativos',
    'ContratosConveniosInteradministrativosValorCero': 'Contratos/Convenios Interadministrativos',
    'PluralityContractsDevelopment': 'Servicios Profesionales',
    'Arrendamiento o Adquisición de Inmuebles (Literal I)': 'Arrendamiento de inmuebles',
    'Presupuesto inferior al 10% de la menor cuantía': 'Presupuesto menor al 10% de la Menor Cuantía',
    'Ley 1150 de 2007': 'Ley 1150 de 2007',
    'PluralityPrestacion': 'Servicios Profesionales',
    'Presupuesto menor al 10% de la Menor Cuantía': 'Presupuesto menor al 10% de la Menor Cuantía',
    'Suministro de bienes y servicios de características técnicas uniformes y común utilización': 'B/S características técnicas uniformes',
    'Cuando no Exista Pluralidad de Oferentes en el Mercado (Literal G)':'No pluralidad de oferentes en el mercado',
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
    'Contratos de Encargo Fiduciario que Celebren Entidades Territoriales (Literal F)':'Encargo Fiduciario'
}


# In[43]:


df_PROCESOS_SECOP_II.loc[:,'JUSTIFICACIÓN MODALIDAD GENERAL']=df_PROCESOS_SECOP_II['JUSTIFICACIÓN MODALIDAD DE CONTRATACIÓN'].replace(reemplazos_justificacion_modalidad)
df_PROCESOS_SECOP_II['JUSTIFICACIÓN MODALIDAD GENERAL'].unique()


# In[44]:


df_PROCESOS_SECOP_II['TIPO DE CONTRATO GENERAL'].unique()


# In[45]:


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
    'ND': 'Crédito Público/Empréstito'
}


# In[46]:


df_PROCESOS_SECOP_II.loc[:,'TIPO DE CONTRATO GENERAL']=df_PROCESOS_SECOP_II['TIPO DE CONTRATO'].replace(reemplazos_tipos_de_contrato)
df_PROCESOS_SECOP_II['TIPO DE CONTRATO GENERAL'].unique()


# In[47]:


df_PROCESOS_SECOP_II.loc[:,'ENLACE DEL PROCESO']=df_PROCESOS_SECOP_II['URLPROCESO']


# In[48]:


df_PROCESOS_SECOP_II.loc[:, 'URLPROCESO'] = df_PROCESOS_SECOP_II['URLPROCESO'].astype(str)

def extract_full_url(text):
    match = re.search(r'https?://[^\'\s]+', text)
    if match:
        return match.group(0)
    else:
        return None


df_PROCESOS_SECOP_II.loc[:, 'ENLACE DEL PROCESO'] = df_PROCESOS_SECOP_II['URLPROCESO'].apply(extract_full_url)


# In[49]:


df_PROCESOS_SECOP_II['ENLACE DEL PROCESO']


# In[50]:


df_PROCESOS_SECOP_II['ESTADO RESUMEN'].unique()


# In[51]:


df_PROCESOS_SECOP_II.loc[:,'ESTADO GENERAL']=df_PROCESOS_SECOP_II['ESTADO RESUMEN']


# In[52]:


reemplazos_estados_procesos_s2 = {
    'Presentación de observaciones': 'En plataforma',
    'Presentación de oferta': 'En plataforma',
    'Manifestación de interés (Menor Cuantía)': 'En plataforma',
    'Fase de ofertas': 'En plataforma',
    'Fase de Selección (Presentación de ofertas)': 'En plataforma',
    'Clarification submission': 'En plataforma',
    'No Definido': 'En plataforma',
    'Proceso de ofertas': 'En plataforma',
    'Estimate Phase':'En plataforma',
    'Selección de ofertas (borrador)':'En plataforma'
}


# In[53]:


df_PROCESOS_SECOP_II['ESTADO GENERAL'].replace(reemplazos_estados_procesos_s2, inplace=True)
df_PROCESOS_SECOP_II['ESTADO GENERAL'].unique()


# In[54]:


df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'ESTADO GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'JUSTIFICACIÓN MODALIDAD GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'TIPO DE CONTRATO GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'ESTADO CONTRATO'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['ESTADO GENERAL'] == 'En plataforma', 'ESTADO CONTRATO'] = 'En proceso de contratación'


# In[55]:


cruce_id_proceso.columns


# In[56]:


cruce_id_proceso1 = df_PROCESOS_SECOP_II
contratos_cruce = pd.merge(cruce_id_proceso[['DEPENDENCIA','MODALIDAD GENERAL','TIPO DE CONTRATO GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','DESCRIPCION DEL PROCESO','PROCESO DE COMPRA','REFERENCIA DEL CONTRATO','ESTADO CONTRATO','VALOR DEL CONTRATO','FECHA DE FIRMA','ENLACE DEL PROCESO']],cruce_id_proceso1, left_on='PROCESO DE COMPRA', right_on='ID DEL PORTAFOLIO', how='left')


# In[58]:


contratos_cruce.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/Cruce contratos vs procesos Cota.xlsx')


# In[59]:


contratos_cruce.columns


# In[60]:


contratos_cruce.shape


# In[61]:


cruce_id_proceso.shape


# In[62]:


df_PROCESOS_SECOP_II.shape


# In[63]:


datos_no_encontrados = contratos_cruce[contratos_cruce['FECHA DE PUBLICACIÓN INICIAL'].isnull()]

datos_no_encontrados.shape


# In[64]:


datos_no_encontrados.head()


# In[65]:


datos_no_encontrados.columns


# In[66]:


datos_no_encontrados.loc[:, 'RESPUESTAS AL PROCEDIMIENTO'] = 0
datos_no_encontrados.loc[:, 'ESTADO GENERAL'] = 'Adjudicado'
datos_no_encontrados.loc[:, 'REFERENCIA DEL PROCESO'] = datos_no_encontrados['REFERENCIA DEL CONTRATO_x']
datos_no_encontrados=datos_no_encontrados[['DEPENDENCIA_x','DESCRIPCION DEL PROCESO','PROCESO DE COMPRA_x','REFERENCIA DEL PROCESO','ESTADO GENERAL','REFERENCIA DEL CONTRATO_x','ESTADO CONTRATO_x','MODALIDAD GENERAL_x','FECHA DE FIRMA_x','VALOR DEL CONTRATO_x','RESPUESTAS AL PROCEDIMIENTO','TIPO DE CONTRATO GENERAL_x','JUSTIFICACIÓN MODALIDAD GENERAL_x','ENLACE DEL PROCESO_x']]


# In[67]:


datos_no_encontrados.columns


# In[68]:


print(f'Tamaño del set antes de eliminar los adjudicados sin proveedor: {df_PROCESOS_SECOP_II.shape} ')
#filtro = (df_PROCESOS_SECOP_II['ESTADO RESUMEN'] == 'Adjudicado') & (df_PROCESOS_SECOP_II['REFERENCIA DEL CONTRATO'].isna())
#df_PROCESOS_SECOP_II.drop(df_PROCESOS_SECOP_II[filtro].index, inplace=True)
df_PROCESOS_SECOP_II=df_PROCESOS_SECOP_II[df_PROCESOS_SECOP_II['FECHA DE PUBLICACIÓN INICIAL'].dt.year ==2024]
print(f'Tamaño del set después de eliminar los adjudicados sin proveedor: {df_PROCESOS_SECOP_II.shape}')


# In[69]:


df_PROCESOS_SECOP_II.columns


# In[70]:


df_PROCESOS_SECOP_II=df_PROCESOS_SECOP_II[['DEPENDENCIA','DESCRIPCIÓN DEL PROCEDIMIENTO','ID DEL PORTAFOLIO','REFERENCIA DEL PROCESO','ESTADO GENERAL','REFERENCIA DEL CONTRATO','ESTADO CONTRATO','MODALIDAD GENERAL','FECHA DE PUBLICACIÓN INICIAL','PRECIO BASE','RESPUESTAS AL PROCEDIMIENTO','TIPO DE CONTRATO GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','ENLACE DEL PROCESO']]


# In[71]:


df_PROCESOS_SECOP_II.columns


# In[72]:


columnas=df_PROCESOS_SECOP_II.columns
datos_no_encontrados.columns=columnas


# In[73]:


consolidado_procesos = pd.concat([df_PROCESOS_SECOP_II,datos_no_encontrados])


# In[74]:


consolidado_procesos.shape


# In[75]:


#consolidado_procesos=consolidado_procesos[consolidado_procesos['FECHA DE PUBLICACIÓN INICIAL'].dt.year ==2024]


# In[76]:


consulta = consolidado_procesos['ESTADO GENERAL'].isin(['Adjudicado'])

# Apply the filter to get the 'REFERENCIA DEL CONTRATO' values
filtered_referencias = consolidado_procesos[consulta]['REFERENCIA DEL CONTRATO']

filtered_referencias.unique()


# In[77]:


filter=(consolidado_procesos['ESTADO GENERAL']=='Adjudicado') & (consolidado_procesos['REFERENCIA DEL CONTRATO'].isna())


# In[78]:


consolidado_procesos=consolidado_procesos[~filter]


# In[79]:


consolidado_procesos.shape


# In[80]:


print(consolidado_procesos['FECHA DE PUBLICACIÓN INICIAL'].dt.year.unique())


# In[81]:


consolidado_procesos.shape


# In[82]:


fecha_filtro = pd.Timestamp('2024-06-07')

# Identificar las filas que deben ser eliminadas
condicion = (consolidado_procesos['FECHA DE PUBLICACIÓN INICIAL'] < fecha_filtro) & (consolidado_procesos['ESTADO GENERAL'] == 'En plataforma')

# Eliminar las filas que cumplen con la condición
consolidado_procesos = consolidado_procesos.drop(consolidado_procesos[condicion].index)


# In[83]:


consolidado_procesos.shape


# In[84]:


hay_en_plataforma = consolidado_procesos[consolidado_procesos['ESTADO GENERAL'] == 'En plataforma']

hay_en_plataforma.shape


# In[84]:





# In[85]:


consolidado_procesos=consolidado_procesos.reset_index().drop('index', axis=1)


# In[86]:


# Identificar los valores faltantes en 'ID DEL PORTAFOLIO'
#valores_faltantes = consolidado_procesos['ID DEL PORTAFOLIO'].isna()

# Obtener los índices de las filas con valores faltantes
#indices_faltantes = consolidado_procesos[valores_faltantes].index

# Reemplazar los valores faltantes por la referencia del contrato de 'datos_no_encontrados'
#consolidado_procesos.loc[indices_faltantes, 'ID DEL PORTAFOLIO'] = datos_no_encontrados['REFERENCIA DEL PROCESO']


# In[87]:


#valores_faltantes.shape


# In[88]:


datos_no_encontrados.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/contratos no encontrados 2024 cota.xlsx',sheet_name='contratos no encontrados 2024 cota')
today = date.today()
consolidado_procesos.loc[:,'HOY'] = today
consolidado_procesos=consolidado_procesos.reset_index().drop('index', axis=1)
consolidado_procesos.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/DB.xlsx',sheet_name='DB')
df_contratos_s2_2024.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/Contratos 2024.xlsx',sheet_name='DB')
#consolidado_procesos['HOY'] = pd.to_datetime(consolidado_procesos['HOY'])


# In[89]:


#print(f'Tamaño del set antes de eliminar los REFERENCIA DEL PROCESO Repetidos: {consolidado_procesos.shape} ')
#consolidado_procesos.drop_duplicates(subset='REFERENCIA DEL PROCESO', keep='first', inplace=True)
#print(f'Tamaño del set después de eliminar los REFERENCIA DEL PROCESO Repetidos: {consolidado_procesos.shape}')


# In[90]:


#consolidado_procesos.to_excel('/content/drive/MyDrive/Colab Notebooks/Proyectos personales/DB.xlsx',sheet_name='DB')

