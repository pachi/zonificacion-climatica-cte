# Notas adicionales sobre datos climáticos en formato EPW para CTE DB-HE

## Datos generales

Se usan años que empiezan en lunes y acaban en lunes ([Año común comenzando en lunes](https://es.wikipedia.org/wiki/Anexo:A%C3%B1o_com%C3%BAn_comenzado_en_lunes))

El 2007 fue un año común (no bisiesto) comenzando en lunes. También lo es el 2018. Los archivos climáticos .met se definieron como del 2007.

Las versiones más recientes de E+ y OS fallan con archivos climáticos EPW que antes funcionaban porque se modificó el código y [ahora necesita que el archivo acabe en salto de línea](https://github.com/NREL/EnergyPlus/issues/10064).

## Docs

### Fuentes de datos climáticos

[Oikolab EPW](https://weatherdownloader.oikolab.com/downloader)
[PVGIS](https://re.jrc.ec.europa.eu/pvg_tools/es/)
[White Box Technologies](http://weather.whiteboxtechnologies.com)

### Formato EPW

[Documentación EPW](https://climate.onebuilding.org/papers/EnergyPlus_Weather_File_Format.pdf)
[Programas auxiliares E+ - WeatherConverter](https://bigladdersoftware.com/epx/docs/23-1/auxiliary-programs/index.html)
[Programas auxiliares E+ - EPW data dictionary](https://bigladdersoftware.com/epx/docs/23-1/auxiliary-programs/energyplus-weather-file-epw-data-dictionary.html)
[Programas auxiliares E+ - EPW in CSV format](https://bigladdersoftware.com/epx/docs/23-1/auxiliary-programs/epw-csv-format-in-out.html)

### Weather converter (solo windows)

Programa WeatherConverter de E+ para conversión de archivos climáticos:

- [WeatherConverter](https://github.com/NREL/EnergyPlus/tree/develop/bin/WeatherConverter)

### Elements

Programa Elements de conversión de datos climáticos:

- [Elements](https://bigladdersoftware.com/projects/elements/)
- [Elements - descarga](https://bigladdersoftware.com/projects/elements/downloads.html)

Se puede correr bien en Wine.

### Data-View2d

Programa online muy interesante de visualización de datos climáticos en EPW, incluidos algunos indicadores de confort:

- [DataView2D](https://drajmarsh.bitbucket.io/data-view2d.html)

### Generación de archivos DDY

Ladybug-tools tiene una implementación:

- [Ladybug-tools - generación DDY](https://github.com/ladybug-tools/ladybug-grasshopper/blob/master/ladybug_grasshopper/src/LB%20EPW%20to%20DDY.py)

Hemos reimplementado esta funcionalidad, eliminando todas las dependencias (hemos dejado los cálculos psicrométricos usando un módulo de LBT)

## Procesado pendiente

Tareas pendientes:

- Añadir datos de localidad correctos en encabezado de epw
  - LOCATION,D3_peninsula,-,ESP,CTE_DB_HE,,40.68,-4.13,1,667.0
- Añadir datos de temperatura del suelo en epw
  - GROUND TEMPERATURES,1,2,,,,13.63,13.63,13.63,13.63,13.63,13.63,13.63,13.63,13.63,13.63,13.63,13.63
- Corregir líneas de comentarios del epw
  - COMMENTS 1, Spanish Weather (D3_peninsula) for the Spanish Building Code (CTE DB-HE) checks. Created by Rafael Villar Burke for all CTE reference climates. Generation date: 01/04/2016
  - COMMENTS 2, Ground temperatures generated using mean dry bulb air temperature.
- Poner días de horario de verano:
  - HOLIDAYS/DAYLIGHT SAVINGS,No,3/25,10/28,0
- Generar archivos de diseño DDY para los archivos climáticos

