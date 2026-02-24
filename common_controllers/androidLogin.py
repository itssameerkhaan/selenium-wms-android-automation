# from appium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.options.android import UiAutomator2Options
# import time
# import sys
# import os
# sys.path.append(
#     os.path.abspath(
#         os.path.join(os.path.dirname(__file__), '..')
#     )
# )
# from common_controllers.logger import get_logger 

# logger = get_logger(__name__)

# class Android :
#     def login():

#         try:
#             # caps = {
#             #     "platformName": "Android",
#             #     "automationName": "UiAutomator2",
#             #     "deviceName": "emulator-5554",
#             #     "appium:app": "/apk/app-release.apk",   
#             #     "autoGrantPermissions": True,
#             #     "appium:ignoreHiddenApiPolicyError": True
#             # }



#             caps = {
#                     "platformName": "Android",
#                     "automationName": "UiAutomator2",
#                     "deviceName": "emulator-5554",

#                     "appium:app": "/apk/app-release.apk",
#                     "autoGrantPermissions": True,

#                     "newCommandTimeout": 300,
#                     "adbExecTimeout": 60000,
#                     "uiautomator2ServerInstallTimeout": 60000,
#                     "uiautomator2ServerLaunchTimeout": 60000,

#                     "disableWindowAnimation": True,
#                     "ignoreHiddenApiPolicyError": True,

#                     "waitForIdleTimeout": 0,
#                     "waitForSelectorTimeout": 0
#                 }


#             options = UiAutomator2Options().load_capabilities(caps)

#             driver = webdriver.Remote(
#                 "http://127.0.0.1:4723",
#                 options=options
#             )

#             wait = WebDriverWait(driver, 20)
#             time.sleep(5)
#         except Exception as e:
#             logger.error(f"Faild to do configuraion of android : - {e}")
#             raise

#         logger.info("App Launched Successfully!")

#         try:
#             time.sleep(15)
#             logger.info(f"inserting user name:")
#             wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@text='Username']")))
#             wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Username']"))).send_keys("asis")
#             logger.info(f"inserting password:")
#             wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@text='Password']")))
#             wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Password']"))).send_keys("asis")

#             #clicking connect
#             wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.TextView[@text='Connect']")))
#             wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Connect']"))).click()
#             logger.info(f"loggin successful.....")
#         except Exception as e:
#             logger.error(f"Faild to logging android :")
#             raise

#         time.sleep(5)

#         return driver



from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common_controllers.logger import get_logger

logger = get_logger(__name__)

class Android:

    @staticmethod
    def login():
        caps = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": "emulator-5554",

            "appium:app": "/apk/app-release.apk",
            "autoGrantPermissions": True,

            "newCommandTimeout": 300,
            "adbExecTimeout": 60000,
            "uiautomator2ServerInstallTimeout": 60000,
            "uiautomator2ServerLaunchTimeout": 60000,

            "noReset": True,
            "dontStopAppOnReset": True,
            "disableWindowAnimation": True,
        }

        options = UiAutomator2Options().load_capabilities(caps)

        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        wait = WebDriverWait(driver, 25)

        logger.info("Appium session started")

        APP_PACKAGE = "com.wmsandroid"

        # FORCE APP RESTART
        try:
            if driver.is_app_installed(APP_PACKAGE):
                logger.info("Restarting app...")
                driver.terminate_app(APP_PACKAGE)
                time.sleep(2)
                driver.activate_app(APP_PACKAGE)
        except Exception as e:
            logger.warning(f"App restart skipped: {e}")

        logger.info("App launched")

        # LOGIN
        time.sleep(5)
        try:
            username = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Username']"))
            )
            username.clear()
            username.send_keys("asis")

            password = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[@text='Password']"))
            )
            password.clear()
            password.send_keys("asis")

            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Connect']"))
            ).click()

            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Login failed: {e}")
            driver.quit()
            raise

        return driver

