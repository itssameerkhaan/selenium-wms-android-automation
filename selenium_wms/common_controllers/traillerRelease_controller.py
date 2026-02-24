
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


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


class Trailer:
    @staticmethod
    def trailerRelease(rfid):

        driver = wms_application_logginPage.login()

        logger.info("i am in Trailer Rlease Mode, THANKYOU...")

        options = Options()
        options.add_argument("--disable-notifications")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  

        wait = WebDriverWait(driver, 20)

        try:
            
            shipping = wait.until(EC.visibility_of_element_located((By.XPATH,"//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[9]/a[1]")))
            actions = ActionChains(driver)
            
            actions.move_to_element(shipping).perform()

            trailer_release = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Trailers release']")))
            actions.move_to_element(trailer_release).perform()
            trailer_release.click()

            #inserting rfid
            logger.info(f"inserting RFID :- {rfid}")
            wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='rfidTag']"))).send_keys(rfid)
            #clicking submitt

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']"))).click()
            #clicking all checkbox
            wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@type='checkbox']"))).click()
            #clicking release
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Release']"))).click()
            #clcking confirm yes
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='OK']"))).click()
            #confirming release
            confirm_text = wait.until(EC.visibility_of_element_located((By.XPATH,"//h2[@id='swal2-title']"))).text.strip()
            logger.info(f"Conformation :- {confirm_text}")

        except Exception:
            logger.exception(": Unable to do TRAILER RLEASE :")
            raise