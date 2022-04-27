# zonificacion-climatica-cte

## Zonificación climática localidades españolas según severidades del Código Técnico de la Edificación

El *Código Técnico de la Edificación (CTE)* permite asignar a cada localidad una zona climática, que se obtiene a partir de su capital de provincia y la altitud sobre el nivel del mar.

Las [tablas del Anejo B](https://www.codigotecnico.org/pdf/Documentos/HE/DccHE.pdf) del *Documento básico de Ahorro de Energía del CTE (CTE DB-HE)* recogen esta zonificación y se elaboraron a partir de datos climáticos correspondientes a las capitales de provincia, realizando interpolación geométrica y calculando dos indicadores, la severidad climática de invierno (SCI) y la severidad climática de verano (SCV). Dichas severidades se codifican como zonas climáticas mediante una letra (zona climática de invierno, ZCI) y un número (zona climática de verano, ZCV) que, combinadas, definen una zona climática (ZC).

Esta zonificación climática está vinculada a las exigencias reglamentarias de eficiencia energética de los edificios, especificadas en el *CTE DB-HE*, pero también se utilizan para cuantificar el bono social térmico, etc.

## Propuesta

Puesto que ahora disponemos de datos de satélite más precisos y para cualquier punto georeferenciado, se plantea el ejercicio de obtener la zonificación climática a partir de esa información y hacer un análisis comparativo con la zonificación existente del CTE DB-HE.

Realizar la propuesta mediante criterios de ciencia reproducible.

## Proceso de análisis

- Obtención de datos:
  - Latitud y longitud de municipios a partir del nomenclator oficial del Centro Nacional de Información Geográfica (CNIG):
    - https://datos.gob.es/gl/catalogo/e00125901-spaignngbe
    - http://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=NGMEN
  - Información climática (radiación y temperatura)
    - Año meteorológico tipo (TMY):
    - [PV-GIS (JRC)](https://re.jrc.ec.europa.eu/pvg_tools/en/)
    - API para obtener TMY:
      - `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.409&lon=-3.724&usehorizon=1&browser=1&outputformat=csv&startyear=2005&endyear=2020&userhorizon=&js=1&period=1`
- Cálculo de indicadores
  - índices de severidad climática de invierno (SCI) y verano (SCV)
  - zonas climáticas de invierno (ZCI, una letra) y verano (ZCV, un número), a partir de SCI y SCV
  - zona climática ZC (letra de ZCI y número de ZCV)
    - [Documento de apoyo de climas](https://www.codigotecnico.org/pdf/Documentos/HE/20170202-DOC-DB-HE-0-Climas%20de%20referencia.pdf)
    - Relación de Dorenbos y Pruitt (1974) para el cálculo de la insolación n/N = 2 · (R_g / R_a - 0.25) (http://ocw.upm.es/pluginfile.php/675/mod_label/intro/RADIACION-GLOBAL.pdf)
    - R_g: Radiación solar sobre un plano horizontal (MJ/m².dia) (suma de datos horarios del TMY)
    - R_a: Radiación solar diaria extraterrestre (MJ/m².dia) (cálculo con fórmula de valor diario según día y localización):
      - https://www.fao.org/3/x0490e/x0490e07.htm (ver "Extraterrestrial radiation for daily periods (Ra)")
      - https://github.com/pachi/soljs/blob/master/src/soljs.js
      - http://ocw.upm.es/pluginfile.php/675/mod_label/intro/RADIACION-SOLAR-EXTRATERRESTRE.pdf
    - GD: Grados día (cálculo de datos horarios):
      - <img src="https://render.githubusercontent.com/render/math?math=GD_{T_b} = \sum {{T_b - T_{ah}} \over 24} \cdot \left\lfloor T_b > T_{ah} \right\rfloor">
      <!-- GD_Tb = Sum( ((Tb - Tah) / 24) si Tb > Tah, o 0 si Tb <= Tah). -->
      - https://fornieles.es/gestion-energetica/que-son-los-grados-dia/
      
- Representación de resultados
  - Mapa ZCI
  - Mapa ZCV
  - Mapa de diferencias entre ZCI calculada y de las tablas CTE DB-HE
  - Mapa de diferencias entre ZCV calculada y de las tablas CTE DB-HE

## Herramientas

- Python para el tratamiento previo de datos
- R para la representación de resultados

## Información de los datos y el proceso

### Datos de entrada

- Descripción, cómo están organizados

    - Datos de municipios y geolocalización
        - Fuente: Nomenclator oficial del Centro Nacional de Información Geográfica (CNIG):
            - https://datos.gob.es/gl/catalogo/e00125901-spaignngbe
            - http://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=NGMEN
        - Licencia: Compatible CC-BY-4
        - Tipo de documento: .csv (... Kb)
        - Ruta: datos/ign/MUNICIPIOS.csv
     
    - Información climática
        - Fuente: Joint Research Center (JRC)
            - [PV-GIS (JRC)](https://re.jrc.ec.europa.eu/pvg_tools/en/)
            - API para obtener TMY:
              - `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.409&lon=-3.724&usehorizon=1&browser=1&outputformat=csv&startyear=2005&endyear=2020&userhorizon=&js=1&period=1`
        - Licencia: ??
        - Formato: Año meteorológico tipo (TMY)

- Origen, cómo se descargan
    - 
### Software necesario
- Nombre de los programas y versiones
    - Python 3
- Dependencias relevantes
    - 
### Pasos a ejecutar
- Comandos concretos
- Definición de la secuencia de tareas
    - 1) Mostrar municipios
    - 2) Selección del municipio
    - 3) Descarga de los datos ('TMY_x.csv') con la API ... ('scrap_tmy.py')
    - 4) Generación de los cálculos de los indicadores ('calc_indicators.py').
    - 5) Generación de las representaciones gráficas ('visualizations.py'). 
 
### Resultados
- Descripción de los archivos finales
- Descripción de los resultados y conclusiones
