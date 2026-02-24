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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import random
import json
import time

load_dotenv()
logger = get_logger(__name__)

try:
    driver = wms_application_logginPage.login()
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)
except Exception as e:
    logger.error(f"Driver initialization failed: {e}")
    sys.exit(1)

FILE_PATH = "C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data"
# FILE_PATH = os.getenv("FILE_PATH")
folder_id = ''.join([str(random.randint(0, 9)) for _ in range(7)])

def create_xml():
    try:
        with open(f"{FILE_PATH}\\silo.json", "r") as f:
            data = json.load(f)
        
        tree = ET.parse(f"{FILE_PATH}\\Silo_Repacking.xml")
        root = tree.getroot()
        
        elements = [
            (".//SPEC_REPACKING_CREATION", "folder", folder_id),
            (".//SPEC_ORIGINAL_MATERIAL_CODE", "text", data.get("product_imc_id")),
            (".//SPEC_FINAL_MATERIAL_CODE", "text", data.get("product_id")),
            (".//SPEC_SILO_NUMBER", "text", data.get("silo_no")),
            (".//SPEC_BATCH", "text", data.get("batch"))
        ]
        
        for tag, attr_type, value in elements:
            element = root.find(tag)
            if element is not None and value:
                if attr_type == "folder":
                    element.set("folder", value)
                else:
                    element.text = value
        
        return ET.tostring(root, encoding="unicode")
    except (FileNotFoundError, json.JSONDecodeError, ET.ParseError) as e:
        logger.error(f"XML creation failed: {e}")
        return None

def navigate_to_repacking():
    try:
        silo_repacking = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[6]/a")))
        # driver.execute_script("arguments[0].click();", silo_repacking)
        actions.move_to_element(silo_repacking).click().perform()
        
        repacking = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[6]/ul/li[7]/a")))
        # driver.execute_script("arguments[0].click();", repacking)S
        actions.move_to_element(repacking).click().perform()
        logger.info("Navigated to repacking")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Navigation failed: {e}")
        raise

def enter_folder_id():
    try:
        folder_id_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='idFolder']")))
        folder_id_input.clear()
        folder_id_input.send_keys(folder_id)
        folder_id_input.send_keys(Keys.TAB)
        logger.info(f"Entered folder ID: {folder_id}")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Folder ID entry failed: {e}")
        raise

def click_display_button():
    try:
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div/div"))).click()
        neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        ActionChains(driver).move_to_element(neutral_element).perform()
        display_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Display']")))
        # driver.execute_script("arguments[0].click();", display_button)
        display_button.click()
        logger.info("Display button clicked")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Display button click failed: {e}")
        raise

def click_display_icon():
    try:
        display_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='rt-tbody']//div[1]//div[1]//div[2]//*[name()='svg']")))
        # driver.execute_script("arguments[0].click();", display_icon)
        # actions.move_to_element(display_icon).click().perform()
        display_icon.click()
        logger.info("Display icon clicked")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Display icon click failed: {e}")
        raise

def send_to_dcs():
    try:
        # Wait and click on the DCS SVG icon
        dcs_element = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@class='rt-tbody']//div[32]//div[1]//*[name()='svg']"
        )))
        # actions.move_to_element(dcs_element).click().perform()
        dcs_element.click()
        logger.info("Sent to DCS")

        time.sleep(2)

        # Wait and click on the 'Yes' button in confirmation modal
        yes_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[normalize-space()='Yes']"
        )))
        # yes_button.click()
        actions.move_to_element(yes_button).click().perform()
        logger.info("Clicked on 'Yes' button in Send to DCS confirmation modal.")

        time.sleep(10)

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Send to DCS failed: {e}")
        raise




def main():
    xml = None
    try:
        xml = create_xml()
        print(f"XML created: {xml}")
        if not xml:
            logger.error("XML creation failed, exiting")
            return
            
        SiloCustom.Integration(driver=driver, xml=xml)
        logger.info("XML integration completed")
            
        navigate_to_repacking()
        enter_folder_id()
        click_display_button()
        click_display_icon()
        send_to_dcs()
        logger.info("Process completed successfully")
        
    except Exception as e:
        logger.error(f"Process failed: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            logger.warning("Failed to quit driver gracefully")

if __name__ == "__main__":
    main()
    