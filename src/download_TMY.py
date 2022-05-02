"""
download_TMY.py

Llamadas a la API de PVGIS para obtener datos climáticos en formato TMY.
Documentación de la API en:
https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en

Input:
    -i  Código INE del municipio
Output:
    'codINE_tmy.csv': Fichero csv con la información devuelta por la API
Uso:
    python3 download_tmy.py -i codigo_ine_municipio
"""

import argparse
import pandas as pd
import requests
import time
import os

MUNICIPIOS_FILE = "../data/Municipios.csv"
DIR_TMY = "../data/tmy/"

def read_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inecod', 
            help=
            """Codigo INE del municipio de interés.""")

    #parser.print_help()
    args = parser.parse_args()
    ine_cod = str(args.inecod)
        
    return ine_cod

def select_lon_lat_from_ine_cod(ine_cod, df_municipios):
    """
    Devuelve la información de latitud y longitud del municipio al que hace referencia
    el código INE
    Args:
        ine_cod (int)   Código INE del municipio
        df_municipios (pd.Dataframe)    Df con la información relevante sobre los municipios
    Return:
        lat (float)  latitud ETRS89
        lon (float)  longitud ETRS89    
    """
    data = df_municipios.loc[df_municipios['COD_INE'] == ine_cod, 
                ['LONGITUD_ETRS89', 'LATITUD_ETRS89']].values[0]
    lon, lat = data
    return lon, lat

def write_url(lat, lon):
    """
    Compone la url

    Args:
        lat (float) Latitud ETRS89 (en grados decimales).
        lon (float) Longitud ETRS89 (en grados decimales).
    """
    url = "https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat={}&lon={}&outputformat=csv".\
        format(str(lat), str(lon))
    return url


def main():
    
    ine_cod = read_arguments()
    out_file = DIR_TMY + ine_cod + '_tmy.csv'

    # Comprobamos que el fichero no está ya descargado
    if out_file not in os.listdir(DIR_TMY):
        df_municipios = pd.read_csv(MUNICIPIOS_FILE, header=0,
                                    dtype={'COD_INE': str,
                                        'COD_PROV': str,
                                        'PROVINCIA': str,
                                        'NOMBRE_ACTUAL': str,
                                        'LONGITUD_ETRS89': float,
                                        'LATITUD_ETRS89': float,
                                        'ALTITUD': float})

        lon, lat = select_lon_lat_from_ine_cod(ine_cod, df_municipios)
        
        url = write_url(lat, lon)
        data = requests.get(url)
        with open(out_file, 'wb') as f:
            print()
            print("Conectando con '{}'". format(url))
            print()
            print("Descargando información en '{}'".format(out_file))
            print()
            f.write(data.content)
    # Si ya está descargado, informamos
    else:
        print()
        print("La información del municipio {} ya está descargada en '{}'".\
            format(ine_cod, out_file))
        print()
        
    
if __name__=='__main__':
    main()
