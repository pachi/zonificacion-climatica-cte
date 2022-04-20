# zonificacion-climatica-cte
Zonificación climática localidades españolas según severidades del Código Técnico de la Edificación

Esta zonificación climática está vinculado a las exigencias reglamentarias de eficiencia energética de los edificios pero, también, para cuantificar el bono social térmico, etc.

El Código Técnico de la Edificación asigna una zona climática a localidad a partir de su capital de provincia y la altitud sobre el nivel del mar. Esa zona climática se obtiene a partir de dos indicadores, la severidad climática de invierno y la severidad climática de verano, que se codifican, respectivamente, mediante una letra y un número y se obtienen a partir de datos climáticos genéricos.

El [Documento de apoyo de climas](https://www.codigotecnico.org/pdf/Documentos/HE/20170202-DOC-DB-HE-0-Climas%20de%20referencia.pdf) especifica cómo se obtienen esos indicadores.

La [tabla del Anejo I del CTE DB-HE permite clasificar una localidad en función de la capital de provincia y su diferencia de altitud](https://www.codigotecnico.org/pdf/Documentos/HE/DccHE.pdf), para obtener un clima tipo (datos horarios de variables climáticas) que se obtuvo en su momento a partir de datos de capitales de provincia y una interpolación geométrica.

Puesto que ahora tenemos datos más precisos para cualquier punto georeferenciado, se podrían tener resultados de mayor calidad.

El objetivo sería:

- Calcular los índices de severidad climática de verano e invierno.
- La información de radiación y temperatura los sacaríamos del año meteorológico tipo (TMY) que obtenemos de la web PV-GIS del JRC (https://re.jrc.ec.europa.eu/pvg_tools/en/) usando su georeferencia (se puede sacar del INE) y la API de la web PVGIS.
  - API: https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.409&lon=-3.724&usehorizon=1&browser=1&outputformat=csv&startyear=2005&endyear=2020&userhorizon=&js=1&period=1 
- Con los índices de severidad climática de verano y de invierno podemos generar unos mapas de resultados y diferencias.
- También se podría hacer un análisis comparativo con las zonas que resultan de aplicar las tablas del Código Técnico de la Edificación (https://www.codigotecnico.org/pdf/Documentos/HE/DccHE.pdf).
- Adicionalmente, se podría hacer un análisis de cómo se comparan las series temporales corrrespondientes a una zona climática concreta (con la misma severidad de verano e invierno) con los climas tipo para cada zona.



