from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.wms_application_login import wms_application_logginPage
from time import sleep
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
import random
logger = get_logger(__name__)

options = Options()

options.add_argument("--log-level=3")
options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage") 

driver = wms_application_logginPage.login()

class siloIntegration:
    @staticmethod
    

    def Integration(driver):

        try:
            logger.info("getting Integration controller....")

            wait = WebDriverWait(driver, 20)

            Administration = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(Administration).perform()

            file_intigration = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/ul/li[8]/a")))
            actions.move_to_element(file_intigration).perform()
            file_intigration.click()

            # delete = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[1]/div/div[3]/div[3]/button")))
            # print("getting delete button :- ",delete.text)

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='myid']")))


            try:
                if checkbox.is_selected():
                    checkbox.click()
                    logger.info("Checkbox is now unchecked .......")

                    time.sleep(5)
                else:
                    logger.info("Checkbox was already unchecked.....")
            except:
                logger.critical(": Unable to unchake sap posting :")
                exit()
            
            try:
                text_area = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/textarea")))
                time.sleep(10)
                print("calling clear")
                text_area.clear()
                # text_area.send_keys(str(xml))
                time.sleep(10)
                
                # time.sleep(10)
                logger.info("XML inserssion is completed......")
            except Exception:
                logger.exception(": Unable to fill xml in text area :")
            

            
        except Exception:
            logger.exception(": Unable to intigrate XML :")

        

siloIntegration.Integration(driver)


