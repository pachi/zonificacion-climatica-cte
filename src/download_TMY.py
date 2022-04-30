"""Llamadas a la API de PVGIS para obtener datos climáticos en formato TMY.

Documentación de la API en:

https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en
"""

import requests
import time

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
    lat, lon = df_municipios.loc[df_municipios['COD_INE'] == \
                                 ine_cod][['LONGITUD_ETRS89', 'LATITUD_ETRS89']]
    return lat, lon

def write_url(lat, lon):
    """
    Compone la url 
    """
    url = "https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat={}&lon={}".format(str(lat), str(lon))
    return url

def read_arguments():
    
    return ine_cod
    

def main():
    
    ine_cod = read_arguments()
    

    url = https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.409&lon=-3.724&usehorizon=1&browser=1&outputformat=csv&startyear=2005&endyear=2020&userhorizon=&js=1&period=1

    urls = [url]

    for (i, url) in enumerate(urls):
        local_file = './' + i + '.tmy'
        print("Descargando archivo ", i, " en ", local_file)
        data = requests.get(url)
        with open(local_file, 'wb') as file:
            file.write(data.content)
        # La API limita a 1/30s por llamada. Paramos 1/20s en cada llamada para no superar el límite
        time.sleep(0.05)

if __name__=='__main__':
    main()
    
