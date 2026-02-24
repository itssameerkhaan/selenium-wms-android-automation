from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
import pandas as pd
import string
import random
import json
import time
import sys
import os
import re
from time import sleep

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..','..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.androidLogin import Android
from common_controllers.wms_application_login import wms_application_logginPage

logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")



class createProdContainer:

    @staticmethod
    def create(folder) -> list:
        driver = driver = Android.login()
        wait = WebDriverWait(driver, 20)

        #repacking
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Repacking']"))).click()
        time.sleep(2)
        #Load Trailer
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Create prod. container']"))).click()

        #enter folder
        logger.info(f"Using Folder id is :- {folder}")
        enter_folder = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Folder ID ?']"))).clear()
        enter_folder.send_keys(folder)
        #click enter
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='ENTER']"))).click()

        #clicking enter
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()

        containers = []
        i=1
        while i <= 5:
            #entering container number
            starting_con = "039999900"+ str(random.randint(123456000,123456789))
            wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Container']"))).send_keys(starting_con)

            #clicing enter button
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
            logger.info(f"container created successfully :- {starting_con}")
            containers.append(starting_con)
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
            i=i+1
            sleep(5)
        logger.info("Container creation completed :")
        return containers


       

file_path = r"C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data\\FolderId.txt"

with open(file_path, "r") as f:
    folder_id = f.read().strip()

try:
    containers = createProdContainer.create(folder=folder_id)
    container_data = {"containers_created": containers}
    with open("C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data\\containers.json", "w") as f:
        json.dump(container_data, f, indent=2)
except Exception as e:
    logger.error(f"container creaation failed due to :- {e}")
    raise
