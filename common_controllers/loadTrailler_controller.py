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
import time
import sys
import os
import re
from time import sleep

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.androidLogin import Android

logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")



class loadTrailer:

    @staticmethod
    def getBoxes(driver,po) -> list:
        print("sameer")
        wait = WebDriverWait(driver, 20)

        preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[8]/a[1]/span[1]")))
        actions = ActionChains(driver)
        actions.move_to_element(preparation).perform()

        orders = wait.until(EC.element_to_be_clickable((By.XPATH, "//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[8]/ul[1]/li[1]/a[1]")))
        actions.move_to_element(orders).perform()
        orders.click()

        neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        ActionChains(driver).move_to_element(neutral_element).perform()

        print("po number is :- ",po)

        po_order = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
        po_order.send_keys(po)

        submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
        submit.click()
        time.sleep(3)

        all_data = []  # to hold rows

        while True:
            # Wait for table rows to load
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.rt-tbody div.rt-tr-group")))

            # Get all row elements
            rows = driver.find_elements(By.CSS_SELECTOR, "div.rt-tbody div.rt-tr-group")

            for row in rows:
                # Extract all cells (columns) in this row
                cells = row.find_elements(By.CSS_SELECTOR, "div.rt-td")
                row_data = [cell.text.strip() for cell in cells]
                
                if any(row_data):  # only add non-empty rows
                    all_data.append(row_data)

            # Try to go to next page
            try:
                next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next') and not(@disabled)]")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                next_btn.click()
                time.sleep(2)  # wait for next page to load
            except:
                print("No more pages left.")
                break

        # Convert to pandas DataFrame
        max_cols = max(len(row) for row in all_data)  # find maximum number of columns
        # Generate column names A, B, C, 
        col_names = list(string.ascii_uppercase[:max_cols])
        df = pd.DataFrame(all_data, columns=col_names)
        mask = df['I'].isna() | (df['I'].astype(str).str.strip() == '')

        # filter column D where I is empty or null
        filtered_list = list(df.loc[mask, 'D'])
        logger.info(f"The Box which are goin to load are :- {filtered_list}")
        logger.info(f"Total number of Boxes to load is :- {len(filtered_list)}")

        driver.close()
        return filtered_list







    @staticmethod
    def LoadTrailer(rfid,containers):
        global trolley_detail

        logger.info("i am in Load Trailer Mode : Thankyou..... ")

        driver = Android.login()
        wait = WebDriverWait(driver, 20)


        print("Loading these Containers :- ",containers)
        #shipping
        wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Shipping']"))).click()
        time.sleep(2)
        #Load Trailer
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Load trailer']"))).click()

        #enter rfid
        logger.info(f"Using Barcode is :- {rfid}")
        wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter Trailer/Barcode']"))).send_keys(rfid)
        #click enter
        wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()


        #gettig total containers to load
        try :
            total_containers_to_load = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Total container associated']/following-sibling::android.widget.EditText"))).text)
        except TimeoutException:
            envalid_rfid = wait.until(EC.visibility_of_element_located((By.XPATH,'''//android.widget.TextView[
                                                                            contains(@text,'RFID')
                                                                            or contains(@text,'vaid')
                                                                            or contains(@text,'destination')
                                                                            or contains(@text,'already')
                                                                            or contains(@text,'incorrect')
                                                                        ]
                                                                    '''))).text.strip()
            logger.exception(envalid_rfid)
            raise
        except Exception:
            logger.exception(": unbale to fill RFID :")
            raise
        #getting loaded container
        loaded_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='No. of containers']/following-sibling::android.widget.EditText"))).text)
        #getting remaining container
        remainig_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Remaining to load']/following-sibling::android.widget.EditText"))).text)
        logger.info(f"Remaining containers are :- {total_containers_to_load - loaded_container} | Total containers avilable :- {total_containers_to_load} | Loaded containers are :- {loaded_container}")
        reamians = total_containers_to_load - loaded_container
        expected_container = int(wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Expected Container']/following-sibling::android.widget.EditText"))).text)
        containers = list(containers)

        try:
            while expected_container - loaded_container> 0:
                #enter container number
                cont = containers[-1]
                driver.find_element(By.XPATH,"//android.widget.EditText[@text='Enter container no.']").send_keys(containers.pop())
                sleep(2)
                #click enter button

               # wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
                loaded_container_conf = int(driver.find_element(By.XPATH,"//android.widget.TextView[@text='No. of containers']/following-sibling::android.widget.EditText").text)

                if loaded_container_conf == loaded_container:
                    try:
                        container_error = driver.find_element(By.XPATH,'''//android.widget.TextView[
                                                                                contains(@text,'Product')
                                                                                or contains(@text,'destination')
                                                                                or contains(@text,'already')
                                                                                or contains(@text,'incorrect')
                                                                            ]
                                                                        ''').text.strip()
                        if container_error:
                            logger.error(f"Unable to insert container number got error :- {container_error}")
                            raise
                    except:
                        pass
                logger.info(f"length of containers table is  :- {len(containers)} | Loaded contianer is :- {cont}")
                expected_container = expected_container-1
                sleep(2)

            # while True:

            #     # Read remaining count ONCE per cycle
            #     remaining = int(
            #         driver.find_element(
            #             By.XPATH,
            #             "//android.widget.TextView[@text='Remaining to load']/following-sibling::android.widget.EditText"
            #         ).text
            #     )

            #     if remaining == 0:
            #         logger.info("All containers loaded")
            #         break

            #     cont = containers.pop()
            #     logger.info(f"Loading container: {cont}")

            #     # Enter container
            #     field = driver.find_element(
            #         By.XPATH,
            #         "//android.widget.EditText[@text='Enter container no.']"
            #     )
            #     field.clear()
            #     field.send_keys(cont)

            #     # MUST click Enter
            #     # driver.find_element(
            #     #     By.XPATH,
            #     #     "//android.widget.TextView[@text='Enter']"
            #     # ).click()

            #     # Let UI settle
            #     sleep(2)

            #     # Check error WITHOUT wait
            #     try:
            #         error_text = driver.find_element(
            #             By.XPATH,
            #             "//android.widget.TextView[contains(@text,'incorrect') or contains(@text,'already') or contains(@text,'destination')]"
            #         ).text
            #         logger.error(f"Container error: {error_text}")
            #         raise Exception(error_text)
            #     except:
            #         pass

            #     sleep(1)


            logger.info(f"Expected container to load is : - {expected_container-loaded_container}")

            if expected_container - loaded_container == 0:
                #clicking close button
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Close']"))).click()
                #clicking OK in alert 
                try:
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    print("Alert text:", alert.text)  # optional
                    alert.accept()
                    print("Alert accepted successfully.")
                except NoAlertPresentException:
                    print("No alert appeared after clicking close.")
                except Exception as e:
                    print("Error while handling alert:", e)
                #clicking valid 
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Valid']"))).click()
                #intering rfid 
                wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter trailer identification no.']"))).send_keys(rfid)
                #clicking enter
                # wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@id='entercontainer']"))).click()
                #entering seal
                wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Enter seal']"))).send_keys("yes")
                #clicking enter
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
                #clicking valid
                wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Valid']"))).click()

                logger.info("Load Trailer successfull .........")
                driver.quit()
            else:
                logger.exception(": Unable to Load all containers :")
                raise
        except Exception as e:
            # text_error = wait.until(EC.visibility_of_element_located((By.XPATH,"//p[@id='errmsg']"))).text
            # logger.error(f"ERROR IS :- {text_error}")
            logger.error(f"Got the error in Loading :- {e}")
            raise
