from selenium import webdriver
import time, pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def channels():

    

    chromedriver_path = r"C:\Users\ibane\OneDrive\Escritorio\chromedriver-win64\chromedriver.exe"

    # Crear un servicio de Chrome y pasarlo al webdriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)



    driver.get("https://www.pluto.tv")

    time.sleep(10)
    channel_list_div = driver.find_element(By.CLASS_NAME, "channelList-0-2-253")



    scroll_increment = 200  # cantidad de píxeles a desplazarse cada vez
    scroll_pause = 0.5  # pausa en segundos entre desplazamientos

    # Obtener la altura total del contenido dentro del contenedor
    scroll_height = driver.execute_script("return arguments[0].scrollHeight", channel_list_div)
    channels = []
    TimeTable = []
    # Desplazarse de manera incremental
    current_position = 0
    while current_position < scroll_height:
        # Desplazar el contenedor
        driver.execute_script("arguments[0].scrollTop = arguments[1];", channel_list_div, current_position)
        
        # Esperar para dar tiempo a cargar nuevos elementos
        time.sleep(scroll_pause)
        
        # Actualizar la posición actual
        current_position += scroll_increment

        first_child_div = channel_list_div.find_element(By.CSS_SELECTOR, "div:first-child")
        items = first_child_div.find_elements(By.CSS_SELECTOR, "div.channelListItem-0-2-258.channel")
        
        for item in items:
            path1 = item.find_element(By.CSS_SELECTOR, "span:first-child")
            path2 = path1.find_element(By.CSS_SELECTOR, "div[role='rowheader']")
            images_div = ((path2.find_element(By.CSS_SELECTOR, "a:first-child")).find_element(By.CLASS_NAME, "image"))
            cronograma = path1.find_element(By.CLASS_NAME, "timelines")
            cells = cronograma.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")

            
            for cell in cells:
                name = cell.find_element(By.CSS_SELECTOR, "a:first-child")
                link = name.get_attribute("href")
                name = name.find_element(By.CSS_SELECTOR, "div:nth-child(2)")

                name = name.find_element(By.CSS_SELECTOR, "div:first-child")
                duration = name.find_element(By.CLASS_NAME, "rating-vitals-container")


                name = name.find_element(By.CLASS_NAME, "name-container")
                name = name.find_element(By.CLASS_NAME, "name-item").text

                duration = duration.find_element(By.CSS_SELECTOR, "div:first-child").text
                


                TimeTable.append({'Nombre':name, 'Duracion':duration, 'Link':link})
                
            channels.append({'Canal':images_div.get_attribute("aria-label")})

 

    df1 = pd.DataFrame(channels)
    df2 = pd.DataFrame(TimeTable)

    df_unicos = df1.drop_duplicates()

 
    name_file = "Unique_Channels.csv"


    df_unicos.to_csv(name_file, index=False, encoding='utf-8')

    name_file = "TimeTable.csv"
    df2.to_csv(name_file, index=False, encoding='utf-8')
