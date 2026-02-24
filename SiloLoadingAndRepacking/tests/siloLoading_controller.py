import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..','..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.wms_application_login import wms_application_logginPage
from SiloLoadingAndRepacking.tests.siloCustom import SiloCustom
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
import random
import time
import json
import re

logger = get_logger(__name__)
load_dotenv()

try:
    driver = wms_application_logginPage.login()
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)
except Exception as e:
    logger.error(f"Driver initialization failed: {e}")
    sys.exit(1)

FILE_PATH = "C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data"

def navigate_to_silo():
    try:
        silo = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[6]/a")))
        actions.move_to_element(silo).click().perform()
        
        silo_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[6]/ul[1]/li[1]/a[1]")))
        actions.move_to_element(silo_2).click().perform()
        logger.info("Navigated to silo")
    except TimeoutException as e:
        logger.error(f"Silo navigation failed: {e}")
        raise

def get_product_id():
    try:
        config_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[2]/a")))
        actions.move_to_element(config_menu).click().perform()

        product_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[2]/ul/li[8]/a")))
        actions.move_to_element(product_menu).click().perform()

        product_menu2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Products']")))
        actions.move_to_element(product_menu2).click().perform()
        time.sleep(1)
        material_type_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='zMaterialType']")))
        material_type_field.clear()
        material_type_field.send_keys("pp")
        time.sleep(1)
        move_out = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]")))
        actions.move_to_element(move_out).perform()
        time.sleep(1)

        display = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']")))
        actions.move_to_element(display).click().perform()

        description_unit = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div[6]/input")))
        description_unit.clear()
        description_unit.send_keys("PAL")

        product_id_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/div/div[5]")))
        product_imc_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/div/div[7]")))
        
        return {
            "product_id": product_id_element.text.strip(),
            "product_imc_id": product_imc_element.text.strip()
        }
    except TimeoutException as e:
        logger.error(f"Product ID retrieval failed: {e}")
        raise

def create_xml(silo_no):
    try:
        tree = ET.parse(f"C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data\\Silo_Loading.xml")
        root = tree.getroot()
        
        # Generate random values
        batch = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        today = datetime.today().strftime('%Y%m%d')
        unique_no = '0' + ''.join([str(random.randint(0, 9)) for _ in range(5)])
        folder = batch + silo_no + today + " " + unique_no
        
        # Get product data
        product_data = get_product_id()

        # Update PO_CREATION attributes
        po_creation = root.find("PO_CREATION")
        if po_creation is not None:
            po_creation.set("folder", folder)
            po_creation.set("product", product_data["product_imc_id"])
            logger.info(f"Updated PO_CREATION - Folder: {folder}, Product: {product_data['product_id']}")

        # Update PO_NUMBER with folder value
        po_number = root.find(".//PO_NUMBER")
        if po_number is not None:
            po_number.text = folder
            logger.info(f"Updated PO_NUMBER: {folder}")

        # Update SPEC_SILO_NUMBER with silo_no
        silo_number = root.find(".//SPEC_SILO_NUMBER")
        if silo_number is not None:
            silo_number.text = silo_no
            logger.info(f"Updated SPEC_SILO_NUMBER: {silo_no}")
        
        # Update BATCH with generated batch number
        batch_element = root.find(".//CHARACTERISTICS/BATCH")
        if batch_element is not None:
            batch_element.text = batch
            logger.info(f"Updated BATCH: {batch}")

        # Save silo data to JSON file
        silo_data = {
            "silo_no": silo_no,
            "product_id": product_data["product_id"],
            "product_imc_id": product_data["product_imc_id"],
            "batch": batch,
            "folder": folder,
            "po_number": folder
        }
        
        print(f"Silo data: {silo_data}")
        
        # Save to JSON file
        with open(f"{FILE_PATH}\\silo.json", "w") as f:
            json.dump(silo_data, f, indent=4)

        # Save silo number to text file
        with open(f"{FILE_PATH}\\siloNo.txt", "w") as f:
            f.write(silo_no)

        # Return the modified XML as string
        xml_string = ET.tostring(tree.getroot(), encoding="unicode")
        logger.info("XML created successfully")
        return xml_string
        
    except (ET.ParseError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"XML creation failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in XML creation: {e}")
        return None
    


def main():
    try:
        navigate_to_silo()
        
        select_status_fill = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[3]//select[1]")))
        Select(select_status_fill).select_by_visible_text("Released")
        
        move_out = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]")))
        actions.move_to_element(move_out).perform()
        time.sleep(1)

        display = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Display']")))
        display.click()

        select_silo_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div[4]")))
        silo_text = select_silo_number.text.strip()
        
        print(f"Silo number selected: {silo_text}")
        xml = create_xml(silo_text)
        if xml:
            print("Generated XML:\n", xml)  # <-- Add this line to print the XML
            # driver_intigration = test_login()
            SiloCustom.Integration(driver=driver, xml=xml)
            # xml = re.sub(r">\s+<", "><", xml).strip()
            print("xml inserted..............................................\n ", xml)
            # rough.xmlIntigration(xml=xml)
            SiloCustom.Integration(driver=driver,xml=xml)
            logger.info("Process completed successfully")
        else:
            logger.error("XML creation failed")
        
    except (TimeoutException, WebDriverException) as e:
        logger.error(f"Process failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()