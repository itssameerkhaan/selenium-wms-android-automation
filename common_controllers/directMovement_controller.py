
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


import sys
import os
import time
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from time import sleep


options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
logger=get_logger()


class Movement:
    @staticmethod
    def directMovement(batch_no,driver):

        logger.info("i am in Drict movement Mode, THANKYOU...")

        options = Options()
        options.add_argument("--disable-notifications")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  

        wait = WebDriverWait(driver, 20)

        try:
            
            storage = wait.until(EC.visibility_of_element_located((By.XPATH,"//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[5]/a[1]")))
            actions = ActionChains(driver)
            
            actions.move_to_element(storage).perform()

            movement = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[4]/a")))
            actions.move_to_element(movement).perform()

            direct_movement = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[4]/ul/li[7]/a")))
            actions.move_to_element(direct_movement).perform()
            direct_movement.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            container_by_batch = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@name='batch']")))
            container_by_batch.send_keys(batch_no)

            display = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Display']")))
            display.click()

            try:
                select_all = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@type='checkbox']")))
                select_all.click()
            except Exception as e:
                logger.exception(": Unable to select all ")
                raise

            try:
                dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='region_id']")))
                select = Select(dropdown)
                select.select_by_visible_text("WH-SPP products")
            except Exception as e:
                logger.exception(": Unable to select :- WH-SPP product")
                raise
            
            validate = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Validate']")))
            validate.click()

            confirm = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[3]/button[1]")))
            confirm.click()

            while True :
                try:
                    logger.info("Validating............. ")#-------
                    confirm_text = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@id='swal2-content']"))).text
                    logger.info(f"Information :- {confirm_text}")
                    if confirm_text == 'Validated Successfully':#------
                        # logger.info("Direct Movement completed sucessfully......")
                        return f"{[batch_no]} Direct Movement completed sucessfully......"
                except:
                    logger.info("Wait it is taking some time....")
                    
                try:
                    errorText = wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[contains(@style,'color: red') and contains(@style,'font-weight')])[1]")))
                    if errorText.text.strip():
                        raise Exception(f"Direct Movement failed [{batch_no}]: {errorText.text}")
                except TimeoutException:
                    continue
                except Exception as e:
                    logger.exception("Exiting due to error")
                    sys.exit(1)

        except Exception as e:
            logger.exception("Exception occured :-")
            raise

