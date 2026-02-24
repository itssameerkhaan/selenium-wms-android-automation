from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

import sys
import os
from time import sleep

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 

logger = get_logger()

class LogicalGate:
    @staticmethod
    def selectGate(driver):
        logger.info("Entering Logical Gate selection mode...")

        wait = WebDriverWait(driver, 20)

        try:
            # Hover over Configuration > Logical Gates
            config_menu = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[2]/a[1]")))
            ActionChains(driver).move_to_element(config_menu).perform()

            logical_gate = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//a[normalize-space()='Logical gates']")))
            ActionChains(driver).move_to_element(logical_gate).click().perform()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            # Click Display button
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Display']"))).click()

            # Filter "Free" in the Assignment column
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='rt-thead -filters']//div[9]//input[1]"))).send_keys("Free")
            sleep(3)

            gate_selected = False

            while True:
                # Step 1: Get all rows on the current page
                rows = driver.find_elements(By.XPATH, "//div[@class='rt-tr-group']")
                logger.info(f"Found {len(rows)} rows in logical gate table.")

                for row_index, row in enumerate(rows, start=1):
                    radio_buttons = row.find_elements(By.XPATH, ".//input[@type='radio']")
                    if not radio_buttons:
                        continue

                    any_selected = any(rb.is_selected() for rb in radio_buttons)

                    if not any_selected:
                        for col_index, rb in enumerate(radio_buttons, start=1):
                            if rb.is_enabled():
                                try:
                                    rb.click()

                                    # Get description from the "Logical Gate" text column
                                    try:
                                        description_elem = row.find_element(
                                            By.XPATH, ".//div[@role='gridcell'][contains(text(), 'Logical Gate')]")
                                        description = description_elem.text.strip()
                                    except:
                                        description = "N/A"

                                    logger.info(f"Selected Gate:- {col_index} | Logical Gate:- {description}")

                                    # Click Save
                                    try:
                                        save_button = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Save']"))
                                        )
                                        save_button.click()
                                        logger.info("Clicked Save button after selecting gate.")
                                    except TimeoutException:
                                        logger.error("Save button not found or not clickable.")

                                    gate_selected = True
                                    break
                                except Exception as e:
                                    logger.warning(f"Error clicking radio: {e}")
                                    continue
                        if gate_selected:
                            return description

                if gate_selected:
                    break  # Successfully selected and saved a gate, exit loop

                # Step 2: Try clicking the Next button if available and enabled
                try:
                    next_button = driver.find_element(By.XPATH, "//button[normalize-space()='Next']")
                    if not next_button.is_enabled():
                        logger.warning("Reached last page. No available gates found.")
                        break
                    else:
                        # Detect current first row to compare after pagination
                        try:
                            first_row_text = driver.find_element(
                                By.XPATH, "(//div[@class='rt-tr-group'])[1]").text.strip()
                        except:
                            first_row_text = ""

                        next_button.click()
                        logger.info("Clicked Next. Waiting for next page to load...")

                        # Wait until the first row changes (pagination complete)
                        WebDriverWait(driver, 10).until(
                            lambda d: d.find_element(By.XPATH, "(//div[@class='rt-tr-group'])[1]").text.strip() != first_row_text
                        )
                        sleep(1)  # Small buffer for stability

                except Exception as e:
                    logger.warning(f"Next button not found or not clickable: {e}")
                    break

            if not gate_selected:
                logger.warning("No unselected and enabled gate found to click.")

        except Exception as e:
            logger.error(f"Exception occurred in selectGate(): {str(e)}")
            raise
