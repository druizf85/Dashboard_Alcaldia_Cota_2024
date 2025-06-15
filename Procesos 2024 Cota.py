import pandas as pd
from datetime import date
import funciones.funciones_complementarias as fc
from dotenv import load_dotenv
import os

CONTRATOS2024_SECOPII_PATH='INTEGRADO.xlsx'

df_contratos_s2 = pd.read_excel(CONTRATOS2024_SECOPII_PATH,sheet_name='S2')

df_contratos_s2_2024=df_contratos_s2[df_contratos_s2['FECHA DE FIRMA'].dt.year == 2024]

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

base_url_PROCESOS_SECOPII = os.getenv("BASEURL1PROCESOS")


df_PROCESOS_SECOP_II = fc.extract_info_api(base_url_PROCESOS_SECOPII, username, password)

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

df_PROCESOS_SECOP_II.rename(columns=reemplazos_columnas_PROCESOS_SECOPII,inplace=True)

cols=list(df_PROCESOS_SECOP_II.columns)
cols=[x.upper().strip() for x in cols]

df_PROCESOS_SECOP_II.columns = cols

columnas_fecha = ['FECHA DE PUBLICACION DEL PROCESO', 'FECHA DE ULTIMA PUBLICACIÓN', 'FECHA DE PUBLICACION (FASE SELECCION)']

df_PROCESOS_SECOP_II[columnas_fecha] = df_PROCESOS_SECOP_II[columnas_fecha].apply(pd.to_datetime)

df_publicacion = df_PROCESOS_SECOP_II.copy()

df_PROCESOS_SECOP_II.sort_values(by ='FECHA DE PUBLICACION DEL PROCESO',ascending = False,inplace=True)
df_PROCESOS_SECOP_II.drop_duplicates(subset='ID DEL PORTAFOLIO', keep='first', inplace=True)

df_publicacion.sort_values(by ='FECHA DE PUBLICACION DEL PROCESO',ascending = True,inplace=True)
df_publicacion.drop_duplicates(subset='ID DEL PORTAFOLIO', keep='first', inplace=True)
df_publicacion.set_index('ID DEL PORTAFOLIO',inplace=True)

df_PROCESOS_SECOP_II = pd.merge(df_PROCESOS_SECOP_II, df_publicacion['FECHA DE PUBLICACION DEL PROCESO'], left_on='ID DEL PORTAFOLIO', right_index=True, how='left')
df_PROCESOS_SECOP_II.rename(columns={'FECHA DE PUBLICACION DEL PROCESO_y': 'FECHA DE PUBLICACIÓN INICIAL','FECHA DE PUBLICACION DEL PROCESO_x': 'FECHA DE PUBLICACIÓN FINAL'}, inplace=True)

cruce_id_proceso = df_contratos_s2_2024

duplicados_df = df_PROCESOS_SECOP_II['ID DEL PORTAFOLIO'].duplicated().sum()

df_PROCESOS_SECOP_II= df_PROCESOS_SECOP_II.drop_duplicates(subset=['ID DEL PORTAFOLIO'])

duplicados_cruce_id_proceso = cruce_id_proceso['PROCESO DE COMPRA'].duplicated().sum()

cruce_id_proceso= cruce_id_proceso.drop_duplicates(subset=['PROCESO DE COMPRA'])

df_PROCESOS_SECOP_II = pd.merge(df_PROCESOS_SECOP_II, cruce_id_proceso[['FECHA DE FIRMA','FECHA DE INICIO DEL CONTRATO','VALOR DEL CONTRATO','DESTINO GASTO','ID CONTRATO', 'REFERENCIA DEL CONTRATO', 'ESTADO CONTRATO','DOCUMENTO PROVEEDOR', 'PROVEEDOR ADJUDICADO', 'ES GRUPO', 'ES PYME','PROCESO DE COMPRA','DEPENDENCIA','MODALIDAD GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','TIPO DE CONTRATO GENERAL']], left_on='ID DEL PORTAFOLIO', right_on='PROCESO DE COMPRA', how='left')

reemplazos_nombre_entidad = {'ALCALDÍA MUNICIPAL COTA':'ALCALDÍA DE COTA',
                             'CUNDINAMARCA - ALCALDIA MUNICIPIO DE COTA':'ALCALDÍA DE COTA',
                             'ALCALDIA DE COTA':'ALCALDÍA DE COTA',
                             'INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA CUNDINAMARCA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE DE COTA':'IMRD',
                             'CUNDINAMARCA - INSTITUTO MUNICIPAL DE RECREACION Y DEPORTE COTA':'IMRD',
                             'EMPRESA DE SERVICIOS PUBLICOS DE COTA SA ESP':'EMSERCOTA',
                             'CUNDINAMARCA - EMSERCOTA S.A. E.S.P. - COTA':'EMSERCOTA',
                             }


df_PROCESOS_SECOP_II.loc[:,'DEPENDENCIA'] = df_PROCESOS_SECOP_II['ENTIDAD'].replace(reemplazos_nombre_entidad)

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

df_PROCESOS_SECOP_II.loc[:,'MODALIDAD GENERAL'] = df_PROCESOS_SECOP_II['MODALIDAD DE CONTRATACION'].replace(reemplazos_modalidad)

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

df_PROCESOS_SECOP_II.loc[:,'JUSTIFICACIÓN MODALIDAD GENERAL']=df_PROCESOS_SECOP_II['JUSTIFICACIÓN MODALIDAD DE CONTRATACIÓN'].replace(reemplazos_justificacion_modalidad)

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

df_PROCESOS_SECOP_II.loc[:,'TIPO DE CONTRATO GENERAL'] = df_PROCESOS_SECOP_II['TIPO DE CONTRATO'].replace(reemplazos_tipos_de_contrato)

df_PROCESOS_SECOP_II.loc[:,'ENLACE DEL PROCESO'] = df_PROCESOS_SECOP_II['URLPROCESO']

df_PROCESOS_SECOP_II.loc[:, 'URLPROCESO'] = df_PROCESOS_SECOP_II['URLPROCESO'].astype(str)

df_PROCESOS_SECOP_II.loc[:, 'ENLACE DEL PROCESO'] = df_PROCESOS_SECOP_II['URLPROCESO'].apply(fc.extract_full_url)

df_PROCESOS_SECOP_II.loc[:,'ESTADO GENERAL'] = df_PROCESOS_SECOP_II['ESTADO RESUMEN']

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

df_PROCESOS_SECOP_II['ESTADO GENERAL'].replace(reemplazos_estados_procesos_s2, inplace=True)
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'ESTADO GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'JUSTIFICACIÓN MODALIDAD GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'TIPO DE CONTRATO GENERAL'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['MODALIDAD GENERAL'] == 'RFI', 'ESTADO CONTRATO'] = 'RFI'
df_PROCESOS_SECOP_II.loc[df_PROCESOS_SECOP_II['ESTADO GENERAL'] == 'En plataforma', 'ESTADO CONTRATO'] = 'En proceso de contratación'

cruce_id_proceso1 = df_PROCESOS_SECOP_II
contratos_cruce = pd.merge(cruce_id_proceso[['DEPENDENCIA','MODALIDAD GENERAL','TIPO DE CONTRATO GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','DESCRIPCION DEL PROCESO','PROCESO DE COMPRA','REFERENCIA DEL CONTRATO','ESTADO CONTRATO','VALOR DEL CONTRATO','FECHA DE FIRMA','ENLACE DEL PROCESO']],cruce_id_proceso1, left_on='PROCESO DE COMPRA', right_on='ID DEL PORTAFOLIO', how='left')

contratos_cruce.to_excel('Cruce contratos vs procesos Cota.xlsx')

datos_no_encontrados = contratos_cruce[contratos_cruce['FECHA DE PUBLICACIÓN INICIAL'].isnull()]
datos_no_encontrados.loc[:, 'RESPUESTAS AL PROCEDIMIENTO'] = 0
datos_no_encontrados.loc[:, 'ESTADO GENERAL'] = 'Adjudicado'
datos_no_encontrados.loc[:, 'REFERENCIA DEL PROCESO'] = datos_no_encontrados['REFERENCIA DEL CONTRATO_x']
datos_no_encontrados=datos_no_encontrados[['DEPENDENCIA_x','DESCRIPCION DEL PROCESO','PROCESO DE COMPRA_x','REFERENCIA DEL PROCESO','ESTADO GENERAL','REFERENCIA DEL CONTRATO_x','ESTADO CONTRATO_x','MODALIDAD GENERAL_x','FECHA DE FIRMA_x','VALOR DEL CONTRATO_x','RESPUESTAS AL PROCEDIMIENTO','TIPO DE CONTRATO GENERAL_x','JUSTIFICACIÓN MODALIDAD GENERAL_x','ENLACE DEL PROCESO_x']]


df_PROCESOS_SECOP_II = df_PROCESOS_SECOP_II[df_PROCESOS_SECOP_II['FECHA DE PUBLICACIÓN INICIAL'].dt.year ==2024]
df_PROCESOS_SECOP_II = df_PROCESOS_SECOP_II[['DEPENDENCIA','DESCRIPCIÓN DEL PROCEDIMIENTO','ID DEL PORTAFOLIO','REFERENCIA DEL PROCESO','ESTADO GENERAL','REFERENCIA DEL CONTRATO','ESTADO CONTRATO','MODALIDAD GENERAL','FECHA DE PUBLICACIÓN INICIAL','PRECIO BASE','RESPUESTAS AL PROCEDIMIENTO','TIPO DE CONTRATO GENERAL','JUSTIFICACIÓN MODALIDAD GENERAL','ENLACE DEL PROCESO']]

columnas=df_PROCESOS_SECOP_II.columns

datos_no_encontrados.columns = columnas

consolidado_procesos = pd.concat([df_PROCESOS_SECOP_II,datos_no_encontrados])

consulta = consolidado_procesos['ESTADO GENERAL'].isin(['Adjudicado'])

filtered_referencias = consolidado_procesos[consulta]['REFERENCIA DEL CONTRATO']

filter = (consolidado_procesos['ESTADO GENERAL']=='Adjudicado') & (consolidado_procesos['REFERENCIA DEL CONTRATO'].isna())

consolidado_procesos=consolidado_procesos[~filter]

fecha_filtro = pd.Timestamp('2024-06-07')

condicion = (consolidado_procesos['FECHA DE PUBLICACIÓN INICIAL'] < fecha_filtro) & (consolidado_procesos['ESTADO GENERAL'] == 'En plataforma')

consolidado_procesos = consolidado_procesos.drop(consolidado_procesos[condicion].index)

hay_en_plataforma = consolidado_procesos[consolidado_procesos['ESTADO GENERAL'] == 'En plataforma']

consolidado_procesos = consolidado_procesos.reset_index().drop('index', axis=1)

datos_no_encontrados.to_excel('contratos no encontrados 2024 cota.xlsx',sheet_name='contratos no encontrados 2024 cota')

today = date.today()

consolidado_procesos.loc[:,'HOY'] = today
consolidado_procesos = consolidado_procesos.reset_index().drop('index', axis=1)
consolidado_procesos.to_excel('DB.xlsx',sheet_name='DB')

df_contratos_s2_2024.to_excel('Contratos 2024.xlsx',sheet_name='DB')