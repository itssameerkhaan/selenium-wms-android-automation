from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


import random
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


options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
logger=get_logger()


class Trailler:
    @staticmethod
    def traillerAssociation(po_number):
        
        logger.info("i am in Trailer Association Mode, THANKYOU...")

        options = Options()
        options.add_argument("--disable-notifications")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  

        driver = wms_application_logginPage.login()
        wait = WebDriverWait(driver, 20)

        try:
            
            preperation = wait.until(EC.visibility_of_element_located((By.XPATH,"//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[8]/a[1]")))
            actions = ActionChains(driver)
            
            actions.move_to_element(preperation).perform()

            trailler_asociation = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Trailers association']")))
            actions.move_to_element(trailler_asociation).perform()
            trailler_asociation.click()

            try:

                input_PO = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@name='id_prep_order']")))
                input_PO.send_keys(po_number)
            except Exception:
                logger.exception(": Unable to insert Po number :")
                raise

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()
            
            # clicking submit
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']"))).click()
            except Exception:
                logger.exception(": Ubale to click on submit :")
                raise
            
            # clicking trailers
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='active nav-link']"))).click()
            except:
                logger.critical(f"Unable to click Trailers")
                pass

            # clcking edit
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//*[name()='path' and contains(@d,'M402.6 83.')]"))).click()
            except Exception:
                logger.critical(": Unable to click on edit :")
                raise

            #inserting driver name
            logger.info("Inserting Driver Name :- Nadir")
            wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='driver_name']"))).clear()
            wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='driver_name']"))).send_keys("Nadir")

            #inserting RFID
            rfid = str(random.randint(1000,9999))

            try:
                sleep(10)
                avilable_rfid = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='rfid_tag']"))).get_attribute("value")
                if not avilable_rfid:
                    logger.info(f"No any already RFID avilable to take")
                    logger.info(f"Inserting RFID tag :- {rfid}")
                    wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='rfid_tag']"))).clear()
                    wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='rfid_tag']"))).send_keys(rfid)
                else:
                    logger.info(f"RFID vlaue is :- {avilable_rfid}")
            except Exception as e:
                logger.error(f"Unable to fill or get RFID :- {e}")
                raise

            #inserting trailler association tag
            logger.info(f"Trailer identification :- {rfid}")
            wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='trailer_identification']"))).clear()
            wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='trailer_identification']"))).send_keys(rfid)

            #inserting expected value
            expected_container = wait.until(EC.presence_of_element_located((By.NAME, "expected_container_number")))
            placeholder_value = expected_container.get_attribute("placeholder")
            expected_container_int = int(placeholder_value.split(" ")[-1])
            expected_container.send_keys(expected_container_int)
            logger.info(f"Expected container to be takken is :- {expected_container_int}")

            #inserting iqamanumber
            iqama = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='iqama_number']")))
            iqama.send_keys("1234567890")
            logger.info(f"Iqama number is :- 1234567890")


            #clicking save button
            wait.until(EC.element_to_be_clickable((By.XPATH,"//*[name()='path' and contains(@d,'M433.941 1')]"))).click()

            #clicking Associated trailler
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Associated Trailers']"))).click()
            except:
                logger.critical(f"Unable to click Associated tarailer")
                pass
            #confirming 
            try:
                confirm_PO = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div[1]/div/div[8]"))).text.strip()

                driver_name = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div[1]/div/div[6]"))).text.strip()

                if confirm_PO == po_number and driver_name == "Nadir":
                    logger.info("Trailer Association DONE")
                    return rfid

            except TimeoutException:
                try:
                    already_saved_element = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/span")))
                    
                    msg = already_saved_element.text.strip()
                    if "data is already saved" in msg.lower():
                        logger.info(f"DATA ALREADY SAVED: {msg}")
                except TimeoutException:
                    logger.warning("Neither confirmation nor 'Already saved' message appeared.")
                except Exception:
                    logger.exception("Unexpected error while checking 'Already saved' message.")

            except Exception:
                logger.exception("Unexpected error during PO and Driver validation.")
        except:
            logger.error(f"Something got wrong happend please confirm trailler")
            raise