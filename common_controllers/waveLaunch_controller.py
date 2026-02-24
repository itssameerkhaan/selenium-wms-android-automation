from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import random


import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from time import sleep


logger = get_logger(__name__)

options = Options()
options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  


class launch:
    @staticmethod

    def waveLaunch(driver,po,logicalgate):
        
        wait = WebDriverWait(driver, 50)
        wait2 = WebDriverWait(driver,300)

        try:

            logger.info("Now Wave Launch MODE, THANKYOU.....")
            preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[8]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(preparation).perform()

            wave = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Waves']")))
            actions.move_to_element(wave).perform()
            wave.click()

            subbmit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            subbmit.click()


            new = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='New']")))
            new.click()

            create_select = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Create and Select']")))
            create_select.click()

            sleep(2)
            wavelist_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='rt-tbody']//div[1]//div[1]//div[13]//*[name()='svg']")))
            wavelist_add.click()
            sleep(5)

            input_PO = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
            input_PO.send_keys(po)
            sleep(5)

            subbmit2 = wait2.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            subbmit2.click()
            sleep(5)

            wave_detail_add = wait2.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='ADD']")))
            wave_detail_add.click()
            sleep(5)

            back_wavelist= wait2.until(EC.element_to_be_clickable((By.XPATH,"//b[normalize-space()='Back']")))
            back_wavelist.click()
            sleep(5)

            launch_wave = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@role='gridcell']//div//*[name()='svg']")))
            launch_wave.click()
            sleep(5)

            wearhous = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='WH']")))
            wearhous.click()
            sleep(5)

            try:
                gate_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "gate")))
                select = Select(gate_dropdown)

                target_gate = logicalgate
                found = False

                # Try to find "from saved gate"
                for option in select.options:
                    if option.text.strip() == target_gate:
                        select.select_by_visible_text(option.text)
                        logger.info(f"Selected gate: {option.text}")
                        found = True
                        break

                # If not found, select a random option (excluding first if it's placeholder)
                if not found:
                    logger.warning(f"{target_gate} not found. Selecting a random gate instead.")
                    options = select.options[1:] if len(select.options) > 1 else select.options
                    random_option = random.choice(options)
                    select.select_by_visible_text(random_option.text)
                    logger.info(f"Randomly selected gate: {random_option.text}")

            except Exception as e:
                logger.error(f"Gate selection failed: {str(e)}")
                raise
            
            sleep(2)

            try:
                ohk = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='OK']")))
                ohk.click()
                logger.info("Launching..........")
            except Exception as e:
                logger.error(f"Failed to click OK button: {e}")
                raise

            def launched_or_failed(driver):
                try:
                    error_elem = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]")
                    if "Request failed with status code 400" in error_elem.text:
                        return "error"
                except:
                    pass

                try:
                    launch_elem = driver.find_element(By.XPATH, "//span[normalize-space()='Launched']")
                    if "Launched" in launch_elem.text:
                        return "launched"
                except:
                    pass

                return False 

            try:
                result = wait2.until(launched_or_failed)

                if result == "error":
                    logger.critical(": Wave Launch Failed | DELETE DOCUMENT WAIT :")
                    raise Exception("Wave launch failed due to status code 400")

                elif result == "launched":
                    return result

            except TimeoutException:
                print("Timeout: Wave not launched and no error appeared.")
            except Exception as e:
                logger.exception(e)
                raise

        except Exception:
            logger.exception(": Wave launch FAILD :")
            raise