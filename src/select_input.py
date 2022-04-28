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

import pandas as pd

if __name__ == "__main__":
    print("Cargando datos de municipios...")
    df = pd.read_csv('../data/ign/MUNICIPIOS.csv',
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

    df['ARCHIVO_TMY'] = df['COD_INE'].apply(lambda x: '{}.tmy'.format(x))

    df.to_csv("../data/output/Municipios.csv", index=False)
    print("Datos de {} municipios cargados.".format(len(df)))
