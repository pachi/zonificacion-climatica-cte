import requests
import time

url = https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.409&lon=-3.724&usehorizon=1&browser=1&outputformat=csv&startyear=2005&endyear=2020&userhorizon=&js=1&period=1

urls = [url]

for (i, url) in enumerate(urls):
    local_file = './' + i + '.tmy'
    print("Descargando archivo ", i, " en ", local_file)
    data = requests.get(url)
    with open(local_file, 'wb') as file:
        file.write(data.content)
    time.sleep(1) # para para no abusar del servidor
