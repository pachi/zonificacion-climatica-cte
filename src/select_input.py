# encoding: utf-8

"""Selección de datos de entrada de los municipios

Selecciona los datos de entrada relevantes del archivo
`data/ign/MUNICIPIOS.csv` del IGN y genera el archivo de
datos `data/output/Municipios.csv` que contendría:

- COD_INE
- COD_PROV
- PROVINCIA
- NOMBRE_ACTUAL
- LONGITUD_ETRS89
- LATITUD_ETRS89
- ALTITUD
- ARCHIVO_TMY
"""

from tabnanny import verbose
import pandas as pd
import os

#from download_TMY import MUNICIPIOS_FILE

MUNICIPIOS_FILE = "data/ign/MUNICIPIOS.csv"
MUNICIPIOS_FILE_FORMATTED = "data/output/Municipios.csv"

if __name__ == "__main__":
    print("Cargando datos de municipios...")
    df = pd.read_csv(MUNICIPIOS_FILE,
                        encoding='latin1',
                        sep=';',
                        decimal=',',
                        dtype={'COD_INE': str,
                            'ID_REL': str,
                            'COD_GEO': str,
                            'COD_PROV': str,
                            'PROVINCIA': str,
                            'NOMBRE_ACTUAL': str,
                            'POBLACION_MUNI': int,
                            'SUPERFICIE': float,
                            'PERIMETRO': float,
                            'COD_INE_CAPITAL': str,
                            'CAPITAL': str,
                            'POBLACION_CAPITAL': int,
                            'HOJA_MTN25_ETRS89': str,
                            'LONGITUD_ETRS89': float,
                            'LATITUD_ETRS89': float,
                            'ORIGENCOOR': str,
                            'ALTITUD': float,
                            'ORIGENALTITUD': str
                            },
                        usecols=[
                            'COD_INE', 'COD_PROV', 'PROVINCIA', 'NOMBRE_ACTUAL',
                            'LONGITUD_ETRS89', 'LATITUD_ETRS89', 'ALTITUD']
                        )

    # Sustituimos los nombres con / para generar un nombre de arcivo válido
    df['ARCHIVO_TMY'] = df[['COD_INE', 'NOMBRE_ACTUAL']].\
        apply(lambda x: '{}_{}.csv'.format(x[0], x[1].replace("/", "__")), axis=1)

    if not os.path.isdir('data/output'):
        os.makedirs('data/output')

    df.to_csv(MUNICIPIOS_FILE_FORMATTED, index=False, encoding='utf-8')
    print("Datos de {} municipios cargados.".format(len(df)))
