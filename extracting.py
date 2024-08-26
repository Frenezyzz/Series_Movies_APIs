from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time



def extracting_apis ():
    chrome_options = Options()
    

    chromedriver_path = r"C:\Users\ibane\OneDrive\Escritorio\chromedriver-win64\chromedriver.exe"
    
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('https://pluto.tv/latam/on-demand')
    time.sleep(8)   

    container = (driver.find_element(By.ID, "root"))
    container = container.find_element(By.CSS_SELECTOR, "div:first-child")
    container = container.find_element(By.CSS_SELECTOR, "div:first-child")
    container = container.find_element(By.CSS_SELECTOR, "div:nth-child(2)")
    container = container.find_element(By.TAG_NAME, "main")
    container = container.find_element(By.CLASS_NAME, "onDemandGuideLayoutContainer-0-2-235")

    container = container.find_element(By.CLASS_NAME, "onDemandGuideContainer-0-2-232")
    container = container.find_element(By.CLASS_NAME, "catalogContainer-0-2-237")

    container = container.find_element(By.CSS_SELECTOR, "div:first-child")
    container = container.find_element(By.CSS_SELECTOR, "div:first-child")
    container = container.find_element(By.CSS_SELECTOR, "div:first-child")
    scroll_height = driver.execute_script("return arguments[0].scrollHeight", container)


    container.click()



    current_position = 0
    scroll_increment = 200  
    scroll_pause = 1 
   

    api_data = []
    while current_position < scroll_height:
        
        driver.execute_script("arguments[0].scrollTop = arguments[1];", container, current_position)      
        time.sleep(scroll_pause)      
        current_position += scroll_increment
       
        logs = driver.get_log('performance')

       
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.requestWillBeSent':
                url = log['params']['request']['url']
                if 'headers' in log['params']['request']:
                    headers = log['params']['request']['headers']
                    authorization = headers.get('Authorization', 'No Authorization Header Found')
                else:
                    authorization = 'No Authorization Header Found'

                if "items?offset=30&page=1" in url:  

                    api_data.append({'URL': url, 'Authorization': authorization})

                    print(f"API URL: {url}")
    return api_data



