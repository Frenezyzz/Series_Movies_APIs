from selenium import webdriver
import time, pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException





def series_chapters(serie):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--disable-gpu")  # Desactivar la GPU para mayor compatibilidad
    chrome_options.add_argument("--window-size=1920x1080")  # Definir un tamaño de ventana
    chrome_options.add_argument("--no-sandbox")  # Agregar esta opción si se ejecuta en un entorno de servidor
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas en entornos de bajo almacenamiento compartido

    chromedriver_path = r"C:\Users\ibane\OneDrive\Escritorio\chromedriver-win64\chromedriver.exe"

    # Crear un servicio de Chrome y pasarlo al webdriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(f"https://pluto.tv/latam/on-demand/series/{serie}/season/1?lang=en")
    time.sleep(10)
    start_time = time.time()
    chapters = driver.find_element(By.ID, "overlay-container")
    chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
    chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
    chapters = chapters.find_element(By.CSS_SELECTOR, "div:nth-child(2)")
    chapters = chapters.find_element(By.CSS_SELECTOR, "section:nth-child(2)")
    chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
    chapters = chapters.find_element(By.CLASS_NAME, "inner")
    chapters = chapters.find_element(By.CSS_SELECTOR, "div:nth-child(5)")

    selection = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
    selection = selection.find_element(By.CSS_SELECTOR, "div:first-child")
    selection = selection.find_element(By.CSS_SELECTOR, "select:first-child")
    selection = selection.find_elements(By.TAG_NAME, "option")



    chapters = chapters.find_element(By.CSS_SELECTOR, "section:nth-child(2)")
    chapters = chapters.find_element(By.CSS_SELECTOR, "ul:nth-child(2)")
    chapters = chapters.find_elements(By.TAG_NAME, "li")

    chapter_list = []
    series_data = []

    for opcion in selection:
        opcion.click()
        time.sleep(10)
        chapters = driver.find_element(By.ID, "overlay-container")
        chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
        chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
        chapters = chapters.find_element(By.CSS_SELECTOR, "div:nth-child(2)")
        chapters = chapters.find_element(By.CSS_SELECTOR, "section:nth-child(2)")
        chapters = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
        chapters = chapters.find_element(By.CLASS_NAME, "inner")
        chapters = chapters.find_element(By.CSS_SELECTOR, "div:nth-child(5)")

        selection = chapters.find_element(By.CSS_SELECTOR, "div:first-child")
        selection = selection.find_element(By.CSS_SELECTOR, "div:first-child")
        selection = selection.find_element(By.CSS_SELECTOR, "select:first-child")
        selection = selection.find_elements(By.TAG_NAME, "option")
        chapters = chapters.find_element(By.CSS_SELECTOR, "section:nth-child(2)")
        chapters = chapters.find_element(By.CSS_SELECTOR, "ul:nth-child(2)")
        chapters_list = chapters.find_elements(By.TAG_NAME, "li")

        for chapter in chapters_list:
            

            aux = chapter.find_element(By.CSS_SELECTOR, "a:first-child")
            chapter_list.append(aux)



            name_chapter = aux.find_element(By.CLASS_NAME, "episode-details")
            number = name_chapter.find_element(By.TAG_NAME, "div")
            number = number.find_element(By.CLASS_NAME, "numbers")
            duration = number.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
            number = number.find_element(By.CSS_SELECTOR, "span:first-child").text
            
            chapter_description = name_chapter.find_element(By.CLASS_NAME, "episode-description-atc").text
            name_chapter = aux.find_element(By.TAG_NAME, "h3").text

            series_data.append({'Name':name_chapter, 'Duration':duration, 'Number':number, 'Description':chapter_description})
    return series_data



