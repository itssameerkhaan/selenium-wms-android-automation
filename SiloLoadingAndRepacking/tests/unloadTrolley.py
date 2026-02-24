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



class unloadTrolley:

    @staticmethod
    def unload(trolley_id):
        driver = driver = Android.login()
        wait = WebDriverWait(driver, 20)

        try:
            #mission
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Mission']"))).click()
            #load collection
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Unload collection']"))).click()
            time.sleep(2)
            
            #enter trolley
            # trolley_id = "03999990987654" + str(random.randint(1000, 9999))
            wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Trolley no.']"))).send_keys(trolley_id)
            logger.info(f"Unloading trolley :-  {trolley_id}")
            #click enter
            wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
        except Exception as e:
            logger.error(f"got error in getting unload collection {e}")
            raise
        
        # confirming location
        try:
            location = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Location']/following-sibling::android.widget.EditText"))).text
            wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Confirm Location?']"))).send_keys(location)
            #clicking enter
            wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
        except Exception as e:
            logger.error(f"got error Unable to confirm location {e}")
            raise

        # unload by container
        def unload_by_container(wait):
            try:
                no_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
                while True:
                    no_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
                    if no_container<=2:
                        break
                    container = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Container']/following-sibling::android.widget.EditText"))).text
                    #inserting container
                    wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Confirm Container No?']"))).send_keys(container)
                    #click enter
                    #wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
                    logger.info(f"unloaded container is :- {container} || remainings are {no_container-1}")
            except Exception as e:
                logger.error(f"got error at the time of unload by container - {e}")
                raise

        #unloadig by trolley

        def unload_by_trolley(wait):
            try:
                # trolley = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Trolley']/following-sibling::android.widget.EditText"))).text
                # trolley_element = wait.until(
                #     EC.presence_of_element_located(
                #         (By.XPATH, "//android.widget.TextView[@text='Trolley']/..//android.widget.EditText")
                #     )
                # )

                # trolley = trolley_element.get_attribute("text")
                #inserting trolley
                wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Confirm Container No?']"))).send_keys(trolley_id)
                #click enter
                #wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
                logger.info(f"Now all remaining containers are unloaded by trolley number :- {trolley_id}")
                return True
            except Exception as e:
                logger.error(f"got error at the time of unload by trolley number {e}")
                raise
        
        unload_by_container(wait=wait)
        unload_by_trolley(wait=wait)




with open(
    r"C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data\\trolley.txt",
    "r"
) as f:
    trolley_id = f.read().strip()
bol = unloadTrolley.unload(trolley_id)
if bol == True:
    logger.info(f"ALL CONTAINER IS UNLOADED")

