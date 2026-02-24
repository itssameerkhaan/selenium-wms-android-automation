from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
import pyperclip
import xml.etree.ElementTree as ET
import xml.dom.minidom
import time
from dotenv import load_dotenv

load_dotenv()


logger = get_logger(__name__)

options = Options()
options.add_argument("--log-level=3")
options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage") 

class SiloCustom:
    @staticmethod
    def Integration(driver, xml):
        try:
            wait = WebDriverWait(driver, 20)
            Administration = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(Administration).perform()

            file_intigration = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/ul/li[8]/a")))
            actions.move_to_element(file_intigration).perform()
            file_intigration.click()

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
                raise

            print("type of xml is :- ",type(xml))

            print("xml type is :- ",type(xml))
            pyperclip.copy(str(xml))
            text_area = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/textarea")))
            text_area.clear()
            text_area.click()
            # text_area.send_keys(xml)
            # driver.execute_script("arguments[0].value = arguments[1];", text_area, xml)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            time.sleep(10)
            try:
                intigrate_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[3]/div[3]/button")))
                intigrate_button.click()
                time.sleep(10)
                logger.info("XML inserssion is completed......")
            except:
                logger.error("XML intigrate button FAILD....")
            
            logger.info("Intigrate is clicked")

            try:
                success_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/span")))
                if success_text.text == "File integrated successfully":
                    logger.info("XML integration completed successfully")
                else:
                    logger.warning(f"Integration result: {success_text.text}")
            except:
                logger.error("Unable to varify XML is itigrated or not")
                raise
                
        except Exception as e:
            logger.exception(f"XML integration failed: {e}")