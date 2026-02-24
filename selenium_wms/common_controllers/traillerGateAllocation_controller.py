

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import TimeoutException

import pandas as pd
import random
from time import sleep
import sys
import os
import re

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.androidLogin import Android

logger = get_logger(__name__)


class trailler:
    @staticmethod
    def traillerGateAllocation(rfid):

        driver = Android.login()

        logger.info("I am in Trailler Gate Allocation Mode : Thank you.....")
        wait = WebDriverWait(driver, 20)

        # Click shipping option
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Shipping']"))).click()

        # Click trailler gate allocation option
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Trailer/gate allocation']"))).click()

        # Enter trailer RFID
        wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Trailer/Rfid']"))).send_keys(rfid)

        # Click Enter
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()

        # # Click Valid with retry
        # try:
        #     for attempt in range(3):
        #         try:
        #             valid_btn = wait.until(EC.presence_of_element_located((By.ID, "Valid")))
        #             driver.execute_script("arguments[0].scrollIntoView(true);", valid_btn)
        #             driver.execute_script("arguments[0].click();", valid_btn)
        #             logger.info("Clicked VALID button successfully.")
        #             break
        #         except StaleElementReferenceException:
        #             logger.warning(f"Attempt {attempt+1}: StaleElementReferenceException, retrying...")
        #             sleep(1)
        #     else:
        #         raise Exception("Unable to click VALID button after retries.")
        # except TimeoutException:
        #     try:
        #         already_allocated = wait.until(EC.visibility_of_element_located((By.XPATH, "//body[1]/p[1]"))).text.strip()
        #         logger.error(f"Already allocated message: {already_allocated}")
        #         return  # or raise Exception if you want to stop execution
        #     except Exception:
        #         logger.exception("Unable to fetch already allocated message.")
        #         raise
        # except Exception:
        #     logger.exception(": Unable to validate the TAG :")
        #     raise

        # Extract and enter gate value
        try:
            full_gate = wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Expected gate']/following-sibling::android.widget.EditText"))).text
            match = re.findall(r'\d+', full_gate)

            if match:
                gate = "D" + str(match[-1])
            else:
                raise ValueError(f"No numeric gate found in: {full_gate}")

            # Enter gate and submit
            wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter gate']"))).send_keys(gate)
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()

            logger.info("Gate Allocation is DONE.")
            driver.quit()
        except Exception:
            logger.exception(": Unable to enter gate :")
            raise

        sleep(3)
