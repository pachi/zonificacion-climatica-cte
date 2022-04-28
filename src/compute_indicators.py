"""Calcula indicadores de zonificación climática

Para cada municipio, lee el archivo `data/output/tmy/$[COD_INE}.tmy` y calcula:

- Indicadores obtenidos a partir de datos de los archivos climáticos TMY:
    - GD
    - n_N
    - SCI
    - SCV
    - ZCI_TMY
    - ZCV_TMY
- Indicadores obtenidos a partir del CTE DB-HE:
    - ZCI_CTE_2019
    - ZCV_CTE_2019
- Indicadores resultantes de la comparación entre los anteriores como
  diferencia en niveles de ZC entre TMY y CTE:

    - ZCI_DIFF
    - ZCV_DIFF

Genera un archivo que incluye, además de las columnas del archivo de municipios
de entrada, los anteriores indicadores y lo guarda en `data/output/Results.csv`.
"""

