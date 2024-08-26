import requests, re
from bs4 import BeautifulSoup
from extracting import extracting_apis
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time
import re
import pandas as pd
from chapters import series_chapters
from channels import channels


start_time = time.time()
def mili_to_hours(duration):
    # Tiempo en milisegundos

    # Convertir milisegundos a segundos
    segundos_totales = duration / 1000

    # Calcular horas, minutos y segundos
    horas = int(segundos_totales // 3600)
    minutos = int((segundos_totales % 3600) // 60)
    segundos = int(segundos_totales % 60)

    # Formato completo
    formato_completo = f"{horas} horas, {minutos} minutos"

    return formato_completo


dict_apis = extracting_apis()
data_movies_series = []
for api in dict_apis:

    url = api['URL']
    headers = {
        'Authorization': api['Authorization']
    }

    try:
        time.sleep(0.4)
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        for item in data['items']:
            if item['type'] == 'movie':
                data_movies_series.append({'Name':item['name'],
                              'Description':item['description'],
                              'Duration': mili_to_hours(item['duration']),
                              'Year': re.findall(r'\b\d{4}\b', item['slug'])[0],
                              'Type': item['type'],
                              'ID': item['_id']
                              })
                
                
            if item['type'] == 'serie':
                
                data_movies_series.append({'Name':item['name'],
                              'Description':item['description'],
                              'Duration': mili_to_hours(item['duration']),
                              'Year': re.findall(r'\b\d{4}\b', item['slug'])[0],
                              'Type': item['type'],
                              'ID': item['_id']
                              })
                
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

channels()


end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")

df1 = pd.DataFrame(data_movies_series)

df1 = df1.drop_duplicates()

ids = df1['ID'].tolist()
data_series_chapters = []
for id in ids:
    data_series_chapters.append(series_chapters(id))


name_file = "Series_Peliculas.csv"
df2 = pd.DataFrame(data_series_chapters)
df1.to_csv(name_file, index=False, encoding='utf-8')
name_file = "capitulos.csv"
# Guardar los datos únicos en un archivo CSV
df2.to_csv(name_file, index=False, encoding='utf-8')
