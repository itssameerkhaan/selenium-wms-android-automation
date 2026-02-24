from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common_controllers.logger import get_logger 
from common_controllers.loggin_urls import applications


class wms_application_logginPage:
    def login():
        try :
            options = Options()
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')

            options.add_argument("--disable-notifications")  
            options.add_argument("--no-sandbox")  
            options.add_argument("--disable-dev-shm-usage")  

            webdriver_path = r"C:\edgedriver\msedgedriver.exe"

            logger = get_logger(__name__)

            service = Service(webdriver_path)
            driver = webdriver.Edge(service=service, options=options)
            driver.get(applications.wms_application_url)
            
            logger.info(f"Getting site :- {driver.title}")

            username = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Username']")))
            username.send_keys("asis")

            password = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Password']")))
            password.send_keys("asis")

            login = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Login']")))
            login.click()
            try:
                home = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='tab active']")))
            
                if home.text == "Home":
                    logger.info("Loggin successfull ...")
                    return driver
                else:
                    logger.warning("Loggin Failed...")
                    driver.quit()
            except:
                logger.warning("--Loggin Failed please check credentials--")
        except Exception as e:
            logger.exception("An error occurred")
       
        
