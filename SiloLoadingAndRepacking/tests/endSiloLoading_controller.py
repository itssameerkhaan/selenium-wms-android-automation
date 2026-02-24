import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..','..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.wms_application_login import wms_application_logginPage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
import random
from dotenv import load_dotenv

load_dotenv()

# FILE_PATH = os.getenv("FILE_PATH")
FILE_PATH = "C:\\jenkingsProject\\Android_automation\\main\\SiloLoadingAndRepacking\\reports\\share_data"

SILO_NO_FILE = f"{FILE_PATH}\\siloNo.txt"


driver = wms_application_logginPage.login()
logger = get_logger(__name__)
actions = ActionChains(driver)
wait = WebDriverWait(driver,30)


try:
    logger.info("Navigating to Silo > Clean and Free...")

    # Hover over the "Silo" main menu
    silo_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[6]/a")))
    actions.move_to_element(silo_menu).perform()

    # Wait and click the "Clean and Free" submenu
    clean_and_free = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[6]/ul/li[5]/a")))
    actions.move_to_element(clean_and_free).perform()
    clean_and_free.click()

    logger.info("Successfully clicked on 'Clean and Free' submenu.")

    # # Wait for the content to load - customize this XPath to something visible on that page
    # page_indicator = wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'Clean and Free')]")))
    # logger.info("Clean and Free page loaded successfully.")

    # Add any actions you want here (form fill, button click, validations, etc
    with open(SILO_NO_FILE, "r") as f:
        SiloNo = f.read().strip()
    
    print("silo number is :- ",SiloNo)
    EnterSiloNo = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='siloNumberl3']")))
    EnterSiloNo.send_keys(SiloNo)

    neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    ActionChains(driver).move_to_element(neutral_element).perform()

      # Click the Display button
    display_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Display']")))
    display_button.click()

    logger.info("Clicked on Display button.")

except Exception as e:
    logger.exception("Failed to navigate to or load Clean and Free page.")

try:
    logger.info("Clicking End Loading button...")

    # Locate the outer clickable div that wraps the SVG icon
    end_loading_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//*[name()='path' and contains(@d,'M256 48C14')]/ancestor::div[contains(@class, 'rt-td')]"
    )))

    # Optional: highlight for debugging
    driver.execute_script("arguments[0].style.border='2px solid red'", end_loading_button)

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView(true);", end_loading_button)
    time.sleep(1)

    # Now use Selenium's click — not JS click
    end_loading_button.click()

    logger.info("Successfully clicked End Silo Loading button.")

except Exception as e:
    logger.exception("Failed to click End Loading button.")

    #confirm endSilo

try:
    logger.info("Waiting for confirmation popup...")

    yes_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/button[1]")))
    yes_button.click()

    logger.info("Clicked 'Yes' to confirm End Silo Loading.")

except Exception as e:
    logger.exception("Failed to confirm End Silo Loading by clicking 'Yes'.")



time.sleep(5)
