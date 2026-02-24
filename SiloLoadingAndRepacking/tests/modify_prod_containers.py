from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
import pandas as pd
import string
import random
import json
import time
import sys
import os
import re
from time import sleep

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..','..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.androidLogin import Android

logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")



class modifyProdContainer:

    @staticmethod
    def modify(containers):
        driver = driver = Android.login()
        wait = WebDriverWait(driver, 20)

        #repacking
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Repacking']"))).click()
        time.sleep(2)
        #modify container
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Modify prod. container']"))).click()

        modifyied_containers = []
        for container in containers:
            #inserting container value
            container_insrt = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Container No?']")))
            container_insrt.clear()
            container_insrt.send_keys(container)
            logger.info(f"Modifying container number :- {container}")
            sleep(3)
            #clicking enter
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
            except:
                pass

            #clicking valid 
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Valid']"))).click()
                modifyied_containers.append(container)
                sleep(3)
            except TimeoutException:
                container_error = driver.find_element(By.XPATH,'''//android.widget.TextView[contains(@text,'already') or contains(@text, 'wrong')]
                                                                    ''').text.strip()
                if container_error:
                    logger.critical(f"got exception at the time of container '{container} modification :- {container_error} ")
                    container_insrt.clear()
                    continue
                else:
                    logger.error("Unable to enter container number")
                    raise
            
        if len(modifyied_containers) == 0:
            logger.error("NO any containers are modifyied")
            raise
        logger.info("All containers are modified :")

        
    
with open(
    r"C:\jenkingsProject\Android_automation\main\SiloLoadingAndRepacking\reports\share_data\containers.json",
    "r"
) as f:
    data = json.load(f)

containers = data.get("containers_created", [])
modifyProdContainer.modify(containers=containers)





# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import (
#     TimeoutException,
#     WebDriverException
# )
# import json
# import sys
# import os
# from time import sleep

# sys.path.append(
#     os.path.abspath(
#         os.path.join(os.path.dirname(__file__), '..', '..')
#     )
# )

# from common_controllers.logger import get_logger
# from common_controllers.androidLogin import Android

# logger = get_logger(__name__)

# class modifyProdContainer:

#     @staticmethod
#     def start_new_session():
#         """Start a fresh Appium session"""
#         driver = Android.login()
#         wait = WebDriverWait(driver, 20)
#         return driver, wait

#     @staticmethod
#     def navigate_to_modify_screen(wait):
#         """Navigate to Modify Product Container screen"""
#         wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//android.widget.TextView[@text='Repacking']")
#             )
#         ).click()

#         wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//android.widget.TextView[@text='Modify prod. container']")
#             )
#         ).click()

#     @staticmethod
#     def modify(containers):

#         driver, wait = modifyProdContainer.start_new_session()

#         # Initial navigation
#         try:
#             modifyProdContainer.navigate_to_modify_screen(wait)
#         except TimeoutException:
#             logger.critical("Failed to navigate to Modify Prod Container screen")
#             driver.quit()
#             raise

#         modified_containers = []

#         for container in containers:
#             try:
#                 logger.info(f"Modifying container number :- {container}")

#                 # Locate input field freshly every time
#                 container_input = wait.until(
#                     EC.presence_of_element_located(
#                         (By.XPATH, "//android.widget.EditText[@text='Enter Container No?']")
#                     )
#                 )

#                 container_input.clear()
#                 container_input.send_keys(container)
#                 sleep(1)

#                 # Click Enter (optional)
#                 try:
#                     wait.until(
#                         EC.element_to_be_clickable(
#                             (By.XPATH, "//android.widget.TextView[@text='Enter']")
#                         )
#                     ).click()
#                 except TimeoutException:
#                     logger.warning("Enter button not found, continuing")

#                 # Click Valid
#                 try:
#                     wait.until(
#                         EC.element_to_be_clickable(
#                             (By.XPATH, "//android.widget.TextView[@text='Valid']")
#                         )
#                     ).click()

#                     modified_containers.append(container)
#                     logger.info(f"Container modified successfully :- {container}")
#                     sleep(2)

#                 except TimeoutException:
#                     # Handle validation errors
#                     try:
#                         error_text = driver.find_element(
#                             By.XPATH,
#                             "//android.widget.TextView[contains(@text,'already') "
#                             "or contains(@text,'wrong')]"
#                         ).text.strip()

#                         logger.warning(
#                             f"Container '{container}' skipped due to error :- {error_text}"
#                         )

#                         container_input.clear()
#                         continue

#                     except:
#                         logger.error("Unknown validation error")
#                         continue

#             except WebDriverException as e:
#                 if "instrumentation process is not running" in str(e):
#                     logger.critical("UiAutomator2 crashed — restarting Appium session")

#                     try:
#                         driver.quit()
#                     except:
#                         pass

#                     # Restart session
#                     driver, wait = modifyProdContainer.start_new_session()

#                     # IMPORTANT: re-navigate to same screen
#                     try:
#                         modifyProdContainer.navigate_to_modify_screen(wait)
#                     except TimeoutException:
#                         logger.critical("Failed to re-navigate after restart")
#                         driver.quit()
#                         raise

#                     continue
#                 else:
#                     driver.quit()
#                     raise
#         if not modified_containers:
#             logger.error("No containers were modified")
#             driver.quit()
#             raise Exception("Container modification failed")

#         logger.info(f"All modified containers: {modified_containers}")
#         driver.quit()

# with open(
#     r"C:\jenkingsProject\Android_automation\main\SiloLoadingAndRepacking\reports\share_data\containers.json",
#     "r"
# ) as f:
#     data = json.load(f)

# containers = data.get("containers_created", [])

# if not containers:
#     raise Exception("No containers found in containers.json")

# modifyProdContainer.modify(containers=containers)
