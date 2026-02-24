from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
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
# from common_controllers.wms_application_login import logginPage

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  

logger = get_logger(__name__)

class create_container:
    @staticmethod
    def Create():
        try:
            driver = wms_application_logginPage.login()

            wait = WebDriverWait(driver, 20)

            storage = wait.until(EC.visibility_of_element_located((By.XPATH,"//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[5]/a[1]")))
            actions = ActionChains(driver)
            actions.move_to_element(storage).perform()

            management = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[1]/a")))
            actions.move_to_element(management).perform()

            container_creation = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[5]/ul/li[1]/ul/li[2]/a")))
            actions.move_to_element(container_creation).perform()
            container_creation.click()

            checkbox = driver.find_element(By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[2]/div[2]/input")


            try:
                if checkbox.is_selected():
                    checkbox.click()
                    click_yes = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[3]/button[1]")))
                    click_yes.click()
                else:
                    logger.info("Checkbox was already unchecked.")
            except:
                logger.critical("Unable to unchake sap posting")
                exit()
            
            product_no = "22202450"
            try:
                product = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[5]/div[2]/input")))
                product.send_keys(product_no)
            except:
                logger.critical(": Unable to enter Product Number :")
            confirm_product = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[5]/div[2]/input")))
            if confirm_product.get_attribute("value") == product_no:
                logger.info(f"Using product is :- {product_no}")
            else:
                logger.error(": Product insersion Faild :")


            num = random.randint(10, 20)
            qty_no = str(num)
            try:
                qty = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[3]/div[5]/input")))
                time.sleep(1)
                qty.send_keys(qty_no)
                wait.until(lambda driver: driver.find_element(By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[3]/div[5]/input").get_attribute("value").strip() != "")
            except:
                logger.critical(": Unable to enter Product Quantity :")
            confirm_qty_no = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[3]/div[5]/input")))
            #print("confirm qnatity is :-,",confirm_qty_no.get_attribute("value"))
            if confirm_qty_no.get_attribute("value") == qty_no:
                logger.info(f"Quantity to be prep :- {qty_no}")
            else:
                logger.critical(": Quantity insersion Faild :")


            number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            batch_no = str(number)
            try:
                batch = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[7]/div[2]/div[2]/input")))
                batch.send_keys(batch_no)
            except:
                logger.critical(": Unable to enter Batch Number :")
            confirm_batch_no = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[7]/div[2]/div[2]/input")))
            if confirm_batch_no.get_attribute("value") == batch_no:
                logger.info(f"Batch Number is :- {batch_no}")
            else:
                logger.critical(": Batch insersion Faild :")

            def dropdown_loaded(driver):
                dropdown_element = driver.find_element(By.NAME, "idPackaging")
                select = Select(dropdown_element)
                return len(select.options) > 1  
            wait.until(dropdown_loaded)

            dropdown = Select(driver.find_element(By.NAME, "idPackaging"))
            dropdown.select_by_visible_text("PP PAL 60")

            validate = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[14]/button")))
            validate.click()

            confirm = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[3]/button[1]")))
            confirm.click()

            try_time = 20
            while try_time>0:
                logger.info("Validating ........")
                try:
                    wait.until(EC.text_to_be_present_in_element((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/span[3]"),"Container created successfully"))
                    confirm_container_to_be_created = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/span[3]")))
                    confirm_creation = confirm_container_to_be_created.text
                    logger.info(confirm_container_to_be_created.text)
                    if confirm_creation == "Container created successfully":
                        # with open(r"C:\\jenkingsProject\\Testing_Main\\root_project\\NormalShippingCycle\\reports\\share_data\\batch.txt", "w") as f:
                        #     f.write(batch_no)
                        # with open(r"C:\\jenkingsProject\\Testing_Main\\root_project\\NormalShippingCycle\\reports\\share_data\\quantity.txt", "w") as f:
                        #     f.write(qty_no)
                        return batch_no, qty_no
                except:
                    logger.info("Please wait taking time in validation...")
                    try_time=try_time-1
            
        except Exception as e:
            logger.critical(": Container Creation Failed :")
            logger.exception("Exception Occured")




