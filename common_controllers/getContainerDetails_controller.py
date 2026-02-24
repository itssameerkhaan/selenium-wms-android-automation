
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import datetime

import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.wms_application_login import wms_application_logginPage


options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
logger=get_logger()


class getContainer:
    @staticmethod
    def get(batch_no):

        driver = wms_application_logginPage.login()
        wait = WebDriverWait(driver, 10)

        options = Options()
        options.add_argument("--disable-notifications")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  

        wait = WebDriverWait(driver, 10)

        logger.info("Getting Container Details..........")

        try:
            
            storage = wait.until(EC.visibility_of_element_located((By.XPATH,"//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[5]/a[1]")))
            
            actions = ActionChains(driver)
            
            actions.move_to_element(storage).perform()

            management = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[1]/a")))
            actions.move_to_element(management).perform()

            containers = wait.until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[5]/ul[1]/li[1]/ul[1]/li[1]/a[1]")))#------
            actions.move_to_element(containers).perform()
            containers.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            container_by_batch = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@name='batch']")))
            container_by_batch.send_keys(batch_no)#------

            search_container = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            search_container.click()

            no_total_containers = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/h6")))
            logger.info(f"Total Number of containers is :- {no_total_containers.text}")

            all_data = []

            while True:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rt-tbody")))

                rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']/div[contains(@class, 'rt-tr-group')]")

                for row in rows:
                    cells = row.find_elements(By.XPATH, ".//div[@role='gridcell']")
                    row_data = [cell.text.strip() for cell in cells]
                    all_data.append(row_data)

                try:
                    next_btn = driver.find_element(By.XPATH, "//button[text()='Next']")
                    is_disabled = next_btn.get_attribute("disabled")

                    if is_disabled:
                        break  
                    else:
                        next_btn.click()
                        WebDriverWait(driver, 10).until_not(EC.staleness_of(rows[0]))  
                except Exception as e:
                    logger.exception("Error during pagination:")
                    break
            column_name = ["index","Batch","Container No.","Location","Product","Grade","PLF Container ID","Status","Type","Parent Container","Packaging ID","Weight (KG)","Modified Date","Version","Modified By","Movement Status","Send To SAP","Device Used"]
            Main_df = pd.DataFrame(all_data,columns=column_name)
            Main_df = Main_df.dropna(axis=1, how='all')
            # logger.info(f"Sample of Contianers is \n{Main_df.head()}")
            # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            try:
                driver.quit()
            except:
                pass
            return Main_df


        except Exception as e:
            logger.exception("Exception occured :-")

