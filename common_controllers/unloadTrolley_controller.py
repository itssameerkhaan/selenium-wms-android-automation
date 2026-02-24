from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from appium.options.android import UiAutomator2Options
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
from common_controllers.androidLogin import Android

logger = get_logger(__name__)

def is_ui_crash(e):
    msg = str(e).lower()
    return any(x in msg for x in [
        "socket hang up",
        "could not proxy command",
        "uiautomator2",
        "instrumentation process is not running"
    ])


def restart_session(driver):
    try:
        driver.quit()
    except:
        pass

    time.sleep(5)
    logger.error("UI crashed. Restarting Android session.")
    return None



def Trolley(troll, container_table, index, driver=None):

        if driver is None:
            logger.info("Starting fresh Android session")
            driver = Android.login()

        elif index > 0:
            logger.info("Going back to proceed with another trolley")
            driver.press_keycode(4)
            time.sleep(3)

        
        wait = WebDriverWait(driver,20)
        mission = wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Mission']")))
        mission.click()

        unloadTrolley = wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Unload collection']")))
        unloadTrolley.click()

        logger.info(f"Now going to unload trolley :- {troll}")

        try:
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Trolley no.']"))).send_keys(troll)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
            time.sleep(3)

            try:
                trolley_aready_unloaded = wait.until(
                    EC.visibility_of_element_located((By.XPATH, '''//android.widget.TextView[
                                                                            contains(@text,'Collection')
                                                                            or contains(@text,'container')
                                                                            or contains(@text,'destination')
                                                                            or contains(@text,'already')
                                                                            or contains(@text,'Incorrect')
                                                                        ]
                                                                    '''))
                ).text.strip()
                if trolley_aready_unloaded in [
                    "Collection container [null] without destination.",
                    f"The container [{troll}] has not been found",
                    f"The trolly/container no [{troll}] is Incorrect"
                ]:
                    logger.exception(f"{trolley_aready_unloaded}")
                    # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='back']"))).click()
                    return True, driver
            except TimeoutException:
                pass
        except Exception:
            logger.exception(": Unable to fill trolley number :")
            raise

        try:
            location_value = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Location']/following-sibling::android.widget.EditText"))
            ).text
            wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Confirm Location?']"))).send_keys(location_value)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
            logger.info(f"Location inserted : - {location_value}")
            time.sleep(3)
        except Exception:
            logger.exception(": Unable to confirm location :")
            raise

        progress_value = int(wait.until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
        logger.info(f"Total number of containers to unload :- {progress_value}")

        while True:
            progress_value = int(wait.until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
            logger.info(f"Remaining containers to unload :- {progress_value}")

            try:
                container_no = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Container']/following-sibling::android.widget.EditText"))
                ).text
                logger.info(f"Unloading container number :- {container_no}")
                wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Confirm Container No?']"))
                ).send_keys(container_no)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
                time.sleep(2)
            except Exception as e:
                if is_ui_crash(e):
                    logger.error("UI crash detected inside distribution")
                    # index=0
                    raise
                else:
                    logger.exception(": Unable to insert container number :")
                    raise

            if progress_value - 1 == 0:
                logger.info(f"Trolley {troll} unloaded successfully ")
                return True, driver


class unload:
    @staticmethod

    def trolley_with_retry(troll, container_table, index, driver=None, max_retries=3):
        attempt = 0

        while attempt <= max_retries:
            try:
                result, driver = Trolley(
                    troll=troll,
                    container_table=container_table,
                    index=index,
                    driver=driver
                )
                return result, driver

            except Exception as e:
                if is_ui_crash(e):
                    attempt += 1
                    logger.error(
                        f"UI crash detected. Restarting session. "
                        f"Attempt {attempt}/{max_retries}"
                    )
                    driver = restart_session(driver)
                    continue
                else:
                    raise

        logger.error("Maximum retry limit reached. Stopping execution.")
        exit(1)





    # def Trolley(troll, container_table, index, driver = None):

    #     if index == 0:
    #         driver = Android.login()
    #     else:
    #         logger.info("Going back to proceed with antoher trolley")
    #         driver.press_keycode(4)
    #         time.sleep(3)

        
    #     wait = WebDriverWait(driver,20)
    #     mission = wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Mission']")))
    #     mission.click()

    #     unloadTrolley = wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Unload collection']")))
    #     unloadTrolley.click()

    #     logger.info(f"Now going to unload trolley :- {troll}")

    #     try:
    #         time.sleep(2)
    #         wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Trolley no.']"))).send_keys(troll)
    #         wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
    #         time.sleep(3)

    #         try:
    #             trolley_aready_unloaded = wait.until(
    #                 EC.visibility_of_element_located((By.XPATH, '''//android.widget.TextView[
    #                                                                         contains(@text,'Collection')
    #                                                                         or contains(@text,'container')
    #                                                                         or contains(@text,'destination')
    #                                                                         or contains(@text,'already')
    #                                                                         or contains(@text,'incorrect')
    #                                                                     ]
    #                                                                 '''))
    #             ).text.strip()
    #             if trolley_aready_unloaded in [
    #                 "Collection container [null] without destination.",
    #                 f"The container [{troll}] has not been found"
    #             ]:
    #                 logger.info(f"Trolley already unloaded :- {troll}")
    #                 # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='back']"))).click()
    #                 return True, driver
    #         except TimeoutException:
    #             pass
    #     except Exception:
    #         logger.exception(": Unable to fill trolley number :")
    #         raise

    #     try:
    #         location_value = wait.until(
    #             EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Location']/following-sibling::android.widget.EditText"))
    #         ).text
    #         wait.until(EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Confirm Location?']"))).send_keys(location_value)
    #         wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
    #         logger.info(f"Location inserted : - {location_value}")
    #         time.sleep(3)
    #     except Exception:
    #         logger.exception(": Unable to confirm location :")
    #         raise

    #     progress_value = int(wait.until(
    #         EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
    #     logger.info(f"Total number of containers to unload :- {progress_value}")

    #     while True:
    #         progress_value = int(wait.until(
    #             EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='No Of Containers']/following-sibling::android.widget.EditText"))).text)
    #         logger.info(f"Remaining containers to unload :- {progress_value}")

    #         try:
    #             container_no = wait.until(
    #                 EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Container']/following-sibling::android.widget.EditText"))
    #             ).text
    #             logger.info(f"Unloading container number :- {container_no}")
    #             wait.until(
    #                 EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Enter Confirm Container No?']"))
    #             ).send_keys(container_no)
    #             wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
    #             time.sleep(2)
    #         except Exception as e:
    #             if is_ui_crash(e):
    #                 logger.error("UI crash detected inside distribution")
    #                 raise
    #             else:
    #                 logger.exception(": Unable to insert container number :")
    #                 raise

    #         if progress_value - 1 == 0:
    #             logger.info(f"Trolley {troll} unloaded successfully ")
    #             return True, driver