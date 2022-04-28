# encoding: utf-8

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

import pandas as pd
import multiprocessing as mp

# Tabla de altitudes del CTE HE 2019
# provincia, capital de provincia, altitud de referencia, zc de referencia y rangos de altitud
provincias = [
    {"prov": 'Albacete', "capital": 'Albacete', "zc_ref": 'D3',
        "alt_ranges": [(-999, 450, 'C3'), (450, 950, 'D3'), (950, 9999, 'E1')]},
    {"prov": 'Alacant/Alicante', "capital": 'Alacant/Alicante', "zc_ref": 'B4',
        "alt_ranges":  [(-99, 250, 'B4'), (250, 700, 'C3'), (700, 9999, 'D3')]},
    {"prov": 'Almería', "capital": 'Almería', "zc_ref": 'A4',
        "alt_ranges": [(-999, 100, 'A4'), (100, 250, 'B4'), (250, 400, 'B3'), (400, 800, 'C3'), (800, 9999, 'D3')]},
    {"prov": 'Ávila', "capital": 'Ávila', "zc_ref": 'E1',
        "alt_ranges": [(-999, 550, 'D2'), (550, 850, 'D1'), (850, 9999, 'E1')]},
    {"prov": 'Badajoz', "capital": 'Badajoz', "zc_ref": 'C4',
        "alt_ranges": [(-999, 400, 'C4'), (400, 450, 'C3'), (450, 9999, 'D3')]},
    {"prov": 'Barcelona', "capital": 'Barcelona', "zc_ref": 'C2',
        "alt_ranges": [(-999, 250, 'C2'), (250, 450, 'D2'), (450, 750, 'D1'), (750, 9999, 'E1')]},
    {"prov": 'Bizkaia', "capital": 'Bilbao', "zc_ref": 'C1',
        "alt_ranges":  [(-999, 250, 'C1'), (250, 9999, 'D1')]},
    {"prov": 'Burgos', "capital": 'Burgos', "zc_ref": 'E1',
        "alt_ranges": [(-999, 600, 'D1'), (600, 9999, 'E1')]},
    {"prov": 'Cáceres', "capital": 'Cáceres', "zc_ref": 'C4',
        "alt_ranges": [(-999, 600, 'C4'), (600, 1050, 'D3'), (1050, 9999, 'E1')]},
    {"prov": 'Cádiz', "capital": 'Cádiz', "zc_ref": 'A3',
        "alt_ranges": [(-999, 150, 'A3'), (150, 450, 'B3'), (450, 600, 'C3'), (600, 850, 'C2'), (850, 9999, 'D2')]},
    {"prov": 'Castelló/Castellón', "capital": 'Castelló de la Plana', "zc_ref": 'B3',
        "alt_ranges": [(-999, 50, 'B3'), (50, 500, 'C3'), (500, 600, 'D3'), (600, 1000, 'D2'), (1000, 9999, 'E1'), ()]},
    {"prov": 'Ceuta', "capital": 'Ceuta', "zc_ref": 'B3',
        "alt_ranges": [(-999, 9999, 'B3')]},
    {"prov": 'Ciudad Real', "capital": 'Ciudad Real', "zc_ref": 'D3',
        "alt_ranges": [(-999, 450, 'C4'), (450, 500, 'C3'), (500, 9999, 'D3')]},
    {"prov": 'Córdoba', "capital": 'Córdoba', "zc_ref": 'B4',
        "alt_ranges": [(-999, 150, 'B4'), (150, 550, 'C4'), (550, 9999, 'D3')]},
    {"prov": 'A Coruña', "capital": 'A Coruña', "zc_ref": 'C1',
        "alt_ranges":  [(-999, 200, 'C1'), (200, 9999, 'D1')]},
    {"prov": 'Cuenca', "capital": 'Cuenca', "zc_ref": 'D2',
        "alt_ranges": [(-999, 800, 'D3'), (800, 1050, 'D2'), (1050, 9999, 'E1')]},
    {"prov": 'Girona', "capital": 'Girona', "zc_ref": 'D2',
        "alt_ranges": [(-999, 100, 'C2'), (100, 600, 'D2'), (600, 9999, 'E1')]},
    {"prov": 'Granada', "capital": 'Granada', "zc_ref": 'C3',
        "alt_ranges": [(-999, 50, 'A4'), (50, 350, 'B4'), (350, 600, 'C4'), (600, 800, 'C3'), (800, 1300, 'D3'), (1300, 9999, 'E1')]},
    {"prov": 'Guadalajara', "capital": 'Guadalajara', "zc_ref": 'D3',
        "alt_ranges": [(-999, 950, 'D3'), (950, 1000, 'D2'), (1000, 9999, 'E1')]},
    {"prov": 'Huelva', "capital": 'Huelva', "zc_ref": 'A4',
        "alt_ranges":  [(-999, 50, 'A4'), (50, 150, 'B4'), (150, 350, 'B3'), (350, 800, 'C3'), (800, 9999, 'D3')]},
    {"prov": 'Huesca', "capital": 'Huesca', "zc_ref": 'D2',
        "alt_ranges": [(-999, 200, 'C3'), (200, 400, 'D3'), (400, 700, 'D2'), (700, 9999, 'E1')]},
    {"prov": 'Jaén', "capital": 'Jaén', "zc_ref": 'C4',
        "alt_ranges":  [(-999, 350, 'B4'), (350, 750, 'C4'), (750, 1250, 'D3'), (1250, 9999, 'E1')]},
    {"prov": 'León', "capital": 'León', "zc_ref": 'E1',
        "alt_ranges": [(-999, 9999, 'E1')]},
    {"prov": 'Lleida', "capital": 'Lleida', "zc_ref": 'D3',
        "alt_ranges": [(-999, 100, 'C3'), (100, 600, 'D3'), (600, 9999, 'E1')]},
    {"prov": 'La Rioja', "capital": 'Logroño', "zc_ref": 'D2',
        "alt_ranges": [(-999, 200, 'C2'), (200, 700, 'D2'), (700, 9999, 'E1')]},
    {"prov": 'Lugo', "capital": 'Lugo', "zc_ref": 'D1',
        "alt_ranges": [(-999, 500, 'D1'), (500, 9999, 'E1')]},
    {"prov": 'Madrid', "capital": 'Madrid', "zc_ref": 'D3',
        "alt_ranges": [(-999, 500, 'C3'), (500, 950, 'D3'), (950, 1000, 'D2'), (1000, 9999, 'E1')]},
    {"prov": 'Málaga', "capital": 'Málaga', "zc_ref": 'A3',
        "alt_ranges": [(-999, 100, 'A3'), (100, 300, 'B3'), (300, 700, 'C3'), (700, 9999, 'D3')]},
    {"prov": 'Melilla', "capital": 'Melilla', "altitud_ref": 130, "zc_ref": 'A3',
        "alt_ranges":  [(-999, 9999, 'A3')]},
    {"prov": 'Murcia', "capital": 'Murcia', "zc_ref": 'B3',
        "alt_ranges":  [(-999, 100, 'B3'), (100, 550, 'C3'), (550, 9999, 'D3')]},
    {"prov": 'Ourense', "capital": 'Ourense', "zc_ref": 'D2',
        "alt_ranges": [(-999, 150, 'C3'), (150, 300, 'C2'), (300, 800, 'D2'), (800, 9999, 'E1')]},
    {"prov": 'Asturias', "capital": 'Oviedo', "zc_ref": 'D1',
        "alt_ranges":  [(-999, 50, 'C1'), (50, 550, 'D1'), (550, 9999, 'E1')]},
    {"prov": 'Palencia', "capital": 'Palencia', "zc_ref": 'D1',
        "alt_ranges": [(-999, 800, 'D1'), (800, 9999, 'E1')]},
    {"prov": 'Illes Balears', "capital": 'Palma', "zc_ref": 'B3',
        "alt_ranges": [(-999, 250, 'B3'), (250, 9999, 'C3')]},
    {"prov": 'Navarra', "capital": 'Pamplona/Iruña', "zc_ref": 'D1',
        "alt_ranges": [(-999, 100, 'C2'), (100, 350, 'D2'), (350, 600, 'D1'), (600, 9999, 'E1')]},
    {"prov": 'Pontevedra', "capital": 'Pontevedra', "zc_ref": 'C1',
        "alt_ranges": [(-999, 350, 'C1'), (350, 9999, 'D1')]},
    {"prov": 'Salamanca', "capital": 'Salamanca', "zc_ref": 'D2',
        "alt_ranges": [(-999, 850, 'D2'), (850, 9999, 'E1')]},
    {"prov": 'Gipuzkoa', "capital": 'Donostia/San Sebastián', "zc_ref": 'D1',
        "alt_ranges": [(-999, 400, 'D1'), (400, 9999, 'E1')]},
    {"prov": 'Cantabria', "capital": 'Santander', "zc_ref": 'C1',
        "alt_ranges":  [(-999, 150, 'C1'), (150, 650, 'D1'), (650, 9999, 'E1')]},
    {"prov": 'Segovia', "capital": 'Segovia', "zc_ref": 'D2',
        "alt_ranges": [(-999, 1050, 'D2'), (1050, 9999, 'E1'), ()]},
    {"prov": 'Sevilla', "capital": 'Sevilla', "zc_ref": 'B4',
        "alt_ranges": [(-999, 200, 'B4'), (200, 9999, 'C4')]},
    {"prov": 'Soria', "capital": 'Soria', "zc_ref": 'E1',
        "alt_ranges": [(-999, 750, 'D2'), (750, 800, 'D1'), (800, 9999, 'E1')]},
    {"prov": 'Tarragona', "capital": 'Tarragona', "zc_ref": 'B3',
        "alt_ranges": [(-999, 100, 'B3'), (100, 500, 'C3'), (500, 9999, 'D3')]},
    {"prov": 'Teruel', "capital": 'Teruel', "zc_ref": 'D2',
        "alt_ranges": [(-999, 450, 'C3'), (450, 500, 'C2'), (500, 1000, 'D2'), (1000, 9999, 'E1')]},
    {"prov": 'Toledo', "capital": 'Toledo', "zc_ref": 'C4',
        "alt_ranges": [(-999, 500, 'C4'), (500, 9999, 'D3')]},
    {"prov": 'València/Valencia', "capital": 'València', "zc_ref": 'B3',
        "alt_ranges": [(-999, 50, 'B3'), (50, 500, 'C3'), (500, 950, 'D2'), (950, 9999, 'E1')]},
    {"prov": 'Valladolid', "capital": 'Valladolid', "zc_ref": 'D2',
        "alt_ranges": [(-999, 800, 'D2'), (800, 9999, 'E1')]},
    {"prov": 'Araba/Álava', "capital": 'Vitoria-Gasteiz', "zc_ref": 'D1',
        "alt_ranges": [(-999, 600, 'D1'), (600, 9999, 'E1')]},
    {"prov": 'Zamora', "capital": 'Zamora', "zc_ref": 'D2',
        "alt_ranges": [(-999, 800, 'D2'), (800, 9999, 'E1')]},
    {"prov": 'Zaragoza', "capital": 'Zaragoza', "zc_ref": 'D3',
        "alt_ranges": [(-999, 200, 'C3'), (200, 650, 'D3'), (650, 9999, 'E1')]},
    {"prov": 'Las Palmas', "capital": 'Las Palmas de Gran Canaria', "zc_ref": 'a3',
        "alt_ranges": [(-999, 350, 'a3'), (350, 750, 'A2'), (750, 1000, 'B2'), (1000, 9999, 'C2')]},
    {"prov": 'Santa Cruz de Tenerife', "capital": 'Santa Cruz de Tenerife', "zc_ref": 'a3',
        "alt_ranges": [(-999, 350, 'a3'), (350, 750, 'A2'), (750, 1000, 'B2'), (1000, 9999, 'C2')]},
]

# Índices para búsquedas
cap_index = {v["capital"]: v for v in provincias}
prov_index = {v["prov"]: v for v in provincias}


def findzc(alt, rangoslist):
    """Devuelve zona climática según altitud alt para los rangos en rangoslist"""
    for minv, maxv, zc in rangoslist:
        if minv <= alt < maxv:
            return zc


def findzcalt(alt, provincia):
    """Devuelve zona climática para una altitud en la provincia dada"""
    return findzc(alt, prov_index[provincia]["alt_ranges"])


ZCI_LEVELS = {"a": 1, "A": 2, "B": 3, "C": 4, "D": 5, "E": 6}


def zci_level(zci):
    """Devuelve nivel numérico de zona climática de invierno, para poder hacer comparaciones"""
    return ZCI_LEVELS[zci]


def tmy_indicators(cod, long, lat, alt, tmy_filename):
    """Calcula indicadores a partir de datos de archivo TMY"""
    # TODO: Calcular indicadores a partir de archivos TMY
    # TODO: leyendo datos de ../data/output/tmy

    return {'COD_INE': cod, 'GD': 0, 'n_N': 0.0, 'SCI': 0.0, 'SCV': 0.0, 'ZCI_TMY': 'A', 'ZCV_TMY': 1}


if __name__ == "__main__":
    print("Cargando datos de municipios...")
    df = pd.read_csv('../data/output/Municipios.csv',
                     dtype={'COD_INE': str,
                            'COD_PROV': str,
                            'PROVINCIA': str,
                            'NOMBRE_ACTUAL': str,
                            'LONGITUD_ETRS89': float,
                            'LATITUD_ETRS89': float,
                            'ALTITUD': float,
                            'ARCHIVO_TMY': str
                            }
                     )
    print("Calculando indicadores CTE...")

    # Calcula indicadores de CTE DB-HE 2019
    # los valores se obtienen de la tabla del Apéndice B del CTE DB-HE 2019
    # a partir de la capital de provincia de la localidad y su altitud
    df['ZC_CTE_2019'] = df.apply(
        lambda x: findzcalt(x['ALTITUD'], x['PROVINCIA']), 1)
    df['ZCI_CTE_2019'] = df.apply(lambda x: x['ZC_CTE_2019'][0], 1)
    df['ZCV_CTE_2019'] = df.apply(lambda x: int(x['ZC_CTE_2019'][1]), 1)

    # Calcula indicadores a partir de archivos TMY en ../data/output/tmy
    print("Calculando indicadores TMY...")
    with mp.Pool() as pool:
        values = [(data['COD_INE'], data['LONGITUD_ETRS89'], data['LATITUD_ETRS89'],
                   data['ALTITUD'], data['ARCHIVO_TMY']) for data in df.to_dict('records')]
        indicators = pool.starmap(tmy_indicators, values, chunksize=100)
        indicators_df = pd.DataFrame(indicators)
        df = df.join(indicators_df.set_index('COD_INE'), on='COD_INE')

    # Calcula diferencia de resultados entre indicadores CTE y TMY
    print("Calculando diferencias...")
    df['ZCI_DIFF'] = df.apply(lambda x: zci_level(
        x['ZCI_CTE_2019']), 1) - df.apply(lambda x: zci_level(x['ZCI_TMY']), 1)
    df['ZCV_DIFF'] = df['ZCV_CTE_2019'] - df['ZCV_TMY']

    df.to_csv("../data/output/Results.csv", index=False)
    print("Indicadores de {} municipios calculados".format(len(df)))
