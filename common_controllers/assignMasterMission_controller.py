from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import pandas as pd
import random
import time 


import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from time import sleep
logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  

class assignMaster:
    @staticmethod

    def assignmission(driver,po):

        try:

            wait = WebDriverWait(driver,20)

            storage = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(storage).perform()

            mission = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[3]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(mission).perform()
            
            display = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[3]/ul/li[7]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(display).perform()

            master_mission = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[3]/ul/li[7]/ul/li[4]/a")))
            actions.move_to_element(master_mission).perform()
            master_mission.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            po_input = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
            po_input.send_keys(po)

            logger.info(f"Finding mission by PO : {po}")
            click_display = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Display']")))
            click_display.click()

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rt-tr-group")))
            driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CLASS_NAME, "rt-tbody"))

            rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']/div[@class='rt-tr-group']/div[contains(@class, 'rt-tr')]")
            all_data = []

            for row in rows:
                cells = row.find_elements(By.CLASS_NAME, "rt-td")
                row_data = [cell.text.strip() for cell in cells]

                if not any(row_data):
                    continue
                all_data.append(row_data)

            columns = [
                "ID", "Mission No", "Origins", "Destination", "Trolley", 
                "Preparation Order Id", "Pallet1", "Pallet2", "Pallet3", "Pallet4",
                "Pallet5", "Pallet6", "Priority",
                "Mission ID", "Pallets to take", "Warehouse From", "Warehouse To", 
                "Distributed To", "Status", "Creation date", "Modified date", 
                "Modified By", "User Treat", "Sabic Order Id", 
                "Sabic Delivery Id", "Saudi Kayan Order Id", "Saudi Kayan Delivery Id"
            ]
            df = pd.DataFrame(all_data)
            df.columns=columns
            df = df.dropna(subset=["Mission No"])
            logger.info(f"Mission Numbers and Pallet to Take is :-\n{df[['Mission No','Pallets to take']]}")

            logger.info(f"")
            logger.info(f"Mission_table :- \n{df}")
            time.sleep(3)

            try:
                select_all = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selectAll']")))
                select_all.click()
                sleep(2)
            except Exception as e:
                print("Exception in select all :-")
                logger.critical(": Unable to Select Select_all Option :")
                raise

            try:
                    distributed_to = wait.until(
                        EC.element_to_be_clickable((By.XPATH,"//div[@class='css-1xc3v61-indicatorContainer']//*[name()='svg']"))
                    )
                    distributed_to.click()
                    sleep(2)
                    asis_option = wait.until(
                        EC.element_to_be_clickable((By.XPATH,"//div[@role='listbox']//div[contains(normalize-space(text()), 'asis')]"))
                    )
                    sleep(2)
                    driver.execute_script("arguments[0].click();", asis_option)
                    sleep(2)

                    logger.info(": Successfully selected 'asis' :")

            except Exception as e:
                logger.critical(f": Distribution Failed : {e}")
                raise

            modify = wait.until(
                EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Modification']"))
            )
            modify.click()

            
            try:
                yes_varify = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[3]/button[1]")))
                yes_varify.click()
            except:
                logger.critical(": Unable to varify at end :")
                raise

            while True:
                try:
                    confirm = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Modified!')]")))
                    logger.info(f"Confirmation :- { confirm.text}")
                    return df

                except TimeoutException:
                    print("Waiting for confirmation...")
                    continue
                except Exception as e:
                    logger.exception(": Exiting due to Faild to Assign Mission :")
                    sys.exit(1)


            sleep(10)
        except Exception as e:
            logger.critical(": Unable to assign Master Mission :")
            raise

