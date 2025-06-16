# Caso Práctico - Gestión Contractual - Alcaldia Cota 2024

Integración de Datos para la Contratación Estatal en la Alcaldía de Cota, Cundinamarca.

El caso práctico consite en implementar herramientas analíticas que permitan:

- Visualizar dentro de la plataforma SECOP II el estado de cada proceso contractual y contrataciones realizadas históricamente.
- Identificar cuellos de botella y tiempos de ejecución de tareas.
- Realizar seguimiento a la ejecución de los planes anuales de adquisiciones.
- Entregar información consolidada y confiable a entes de control, ciudadanía, proveedores y directivos.

Contando con experiencia en contratación estatal, conocimiento en lenguajes de programación para manipulación de dataframes, conexiones a APIs y herramientas de visualización analítica como Power BI, se implementó una solución basada en tres puntos:

- Extracción automatizada de datos públicos desde plataformas oficiales (SECOP I, II y TVEC).
- Procesos ETL personalizados, que permitieran transformar y estandarizar la información según criterios técnicos y contractuales definidos.
- Visualizaciones interactivas en Power BI, diseñadas para entregar valor a distintos tipos de usuarios: desde gerentes hasta ciudadanos.

Este enfoque dio lugar a los siguientes informes en Power BI:

INFORME - SEGUIMIENTO A PROCESOS DE CONTRATACIÓN PUBLICADOS

![image](https://github.com/user-attachments/assets/a574111f-c132-454e-add5-0eed96637616)
![image](https://github.com/user-attachments/assets/ac76e5d9-0f54-440d-bdee-2b932c757756)
![image](https://github.com/user-attachments/assets/259b5c7d-b10f-4bed-87f8-3193d4548b55)

Este informe permite consultar a diario el estado de los procesos de contratación publicados en SECOP II. Muestra visualizaciones como:

- Valor y cantidad total de procesos.
- Número de ofertas recibidas.
- Estados del proceso.
- Modalidades y tipos de contrato.
- Justificación de modalidades.
- Búsqueda por número de proceso.
- Valor total de los procesos acumulados por mes.
- Tabla consolidada con los datos esenciales por proceso.

INFORME - CONTRATACIÓN HISTÓRICA

![image](https://github.com/user-attachments/assets/18b9f540-db77-4d55-9377-d3d8a368f14f)
![image](https://github.com/user-attachments/assets/a25177fb-1b58-46aa-ab9e-8536edcada34)
![image](https://github.com/user-attachments/assets/f34fac16-ca50-4be9-81a9-aa5f9eecbc9d)

Integra datos de SECOP I, SECOP II y TVEC. Permite analizar de manera retrospectiva:

- Valor y cantidad de contratos firmados.
- Modalidades de contratación por año.
- Participación por plataforma.
- Clasificación UNSPSC por valor y cantidad.
- Estados de los contratos a lo largo del periodo.
- Tabla consolidada con los datos esenciales por contrato.

INFORME - SEGUIMIENTO CONTRATOS DE PRESTACIÓN DE SERVICIOS (CPS) SECOP II

![image](https://github.com/user-attachments/assets/2f5e2b60-d7e4-4e49-b59e-65795de75da5)
![image](https://github.com/user-attachments/assets/1c884f06-988c-4209-99fa-5185ede6b2a2)

Desarrollado para llevar seguimiento a validaciones específicas de los contratos de prestación de servicios (estado actual y seguimiento a la liquidación de contratos finalizados y alertas al cierre y liquidaci{on de contratos por vencer), dentro de sus visualizaciones se encuentran:

- Cantidad y valor de los contratos por mes.
- Estado de liquidación y cumplimiento sobre la totalidad de contratos finalizados.
- Revisión histórica de estado de los contratos por vigencia.
- Tabla consolidada con los datos esenciales por contrato.

Resultados y logros esperados:

- Reducir la dependencia de hojas de cálculo desactualizadas y poco confiables.
- Implementación de un proceso ETL replicable y adaptable para futuras vigencias.
- Habilitar el acceso abierto a la ciudadanía y entes de control a través de Power BI.
- Generar insumos clave para auditorías, informes de gestión y alertas internas.
