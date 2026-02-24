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

logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")



class loadTrolley:

    @staticmethod
    def load(containers):
        driver = driver = Android.login()
        wait = WebDriverWait(driver, 20)

        try:
            #mission
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Mission']"))).click()
            #load collection
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Load collection']"))).click()
            time.sleep(2)
            
            #enter trolley
            trolley_id = "03999990987654" + str(random.randint(1000, 9999))
            wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Trolley No?']"))).send_keys(trolley_id)
            logger.info(f"Using trolley :-  {trolley_id}")
            #click enter
            wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
        except Exception as e:
            logger.error(f"got error in getting load load collection {e}")
            raise
        
        #inserting container
        try:
            loaded = []
            for container in containers:
                loaded_no_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//*[contains(@text,'No Of Containers')]/following-sibling::android.widget.EditText"))).text)
                insert_container = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Containers ?']")))
                insert_container.send_keys(container)
                # logger.info(f"{container} container loaded")
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
                _load = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//*[contains(@text,'No Of Containers')]/following-sibling::android.widget.EditText"))).text)

                if loaded_no_container == _load:
                    try:
                        container_error = ""
                        container_error = driver.find_element(By.XPATH,'''//android.widget.TextView[contains(@text,'already') or contains(@text, 'wrong')]
                                                                            ''').text.strip()
                    except:
                        pass
                    if container_error:
                        logger.critical(f"{container_error}")
                else:
                    logger.info(f"loaded container is :- {container} || and total loaded is :- {_load}")
                insert_container.clear()
                loaded.append(container)
                sleep(3)
        except Exception as e :
            logger.error(f"got error at the time of load container {e}")
            raise
        
        if len(containers) == len(loaded):
            try:
                #clicking end
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='End']"))).click()
                #clicking back
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Back']"))).click()

                logger.info(f"LOAD TROLLEY SUCCESSFULL")
            except Exception as e:
                logger.error(f"got error in clicking END or BACK {e}")
                raise
            return loaded,trolley_id







with open(
    r"C:\jenkingsProject\Android_automation\main\SiloLoadingAndRepacking\reports\share_data\containers.json",
    "r"
) as f:
    data = json.load(f)

containers = data.get("containers_created", [])
all_loaded,trolley = loadTrolley.load(containers)
with open(r"C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data\\trolley.txt", "w") as f:
            f.write(trolley)
logger.info(f"Lenght of total loaded container is :- {len(all_loaded)}")
