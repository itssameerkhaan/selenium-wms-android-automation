# from appium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

# from appium.options.android import UiAutomator2Options
# from selenium.common.exceptions import TimeoutException

# import pandas as pd
# import random
# import time
# import sys
# import os

# sys.path.append(
#     os.path.abspath(
#         os.path.join(os.path.dirname(__file__), '..')
#     )
# )
# from common_controllers.logger import get_logger 
# from common_controllers.androidLogin import Android

# logger = get_logger(__name__)


# class mission:
#     def get_boxes(po_number,driver):
#         try:
#             logger.info("getting Integration controller....")

#             wait = WebDriverWait(driver, 20)

#             preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[8]/a[1]/span[1]")))
#             actions = ActionChains(driver)
#             actions.move_to_element(preparation).perform()

#             boxes = wait.until(EC.element_to_be_clickable((By.XPATH, "//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[8]/ul[1]/li[1]/a[1]")))
#             actions.move_to_element(boxes).perform()
#             boxes.click()

#             neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
#             ActionChains(driver).move_to_element(neutral_element).perform()

#             po_order = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
#             po_order.send_keys(po_number)

#             submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
#             submit.click()
#             time.sleep(3)

#             data = []

#             while True:
#                 WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, ".rt-tbody .rt-tr-group"))
#                 )

#                 rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")

#                 for row in rows:
#                     cells = row.find_elements(By.CSS_SELECTOR, ".rt-td")

#                     if len(cells) > 10:
#                         box = cells[3].text.strip()
#                         parent_container = cells[8].text.strip()
#                         location = cells[10].text.strip()

#                         data.append({
#                             "Box": box,
#                             "Parent Container No": parent_container,
#                             "Location": location
#                         })

#                 # pagination
#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Next']")
#                     if next_btn.is_enabled():
#                         next_btn.click()
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break
#             #----
#             df = pd.DataFrame(data)

#             boxes_df = df[
#                 (
#                     df["Parent Container No"].isna() |
#                     (df["Parent Container No"].str.strip() == "")
#                 )
#                 &
#                 (df["Box"].notna()) &
#                 (df["Box"].str.strip() != "")
#             ]

#             try:
#                 driver.quit()
#             except:
#                 pass
#             result = dict(zip(boxes_df["Box"], boxes_df["Location"]))
#             return result
#         except:
#             logger.error(f"Unable to get boxes")





#     def distribution(mission,containers):

#         driver = Android.login()
#         wait = WebDriverWait(driver,20)

#         boxes = containers.copy()

#         # click mission
#         wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Mission']"))).click()
#         # click distribution
#         wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Mission distribution']"))).click()

#         logger.info(f"Going to do mission distribution for :- {mission}")

#         # getting mission value
#         missioin_value = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText"))).text
#         current = ""
#         loaded_containers = []
#         trolley_list = []
#         first_mission = missioin_value


#         while first_mission != current:
#             if missioin_value in mission:
#                 logger.info(f"Mission number : {missioin_value} : selected")
#                 #clicking enter 
#                 # containers = [i for i in containers if i not in loaded_containers]
#                 try:
#                     wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
#                 except Exception as e:
#                     logger.error(f"Erron in clicking enter after chossing mission vlaue {e}")
#                     raise

#                 #inserting location
#                 try:
#                     #getting location value
#                     location_vlaue = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Location']/following-sibling::android.widget.EditText"))).text

#                     # extracting boxes for that location 
#                     containers = [
#                         box for box, loc in boxes.items()
#                         if loc == "19@"+location_vlaue
#                     ]
#                     containers = [i for i in containers if i not in loaded_containers]

#                     #sending location value
#                     wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='confirm location?']"))).send_keys(location_vlaue)
#                     # now clicking enter vlaue
#                     wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
#                 except Exception as e:
#                     logger.error(f"Got error in inserting location vlaue :- {e}")
#                     raise

#                 #inserting trolley
#                 try:
#                     #creating trolley number
#                     trolley_num = "03999999123456"
#                     rand = random.randint(1000, 9999)
#                     trolly = trolley_num + str(rand)

#                     #inserting trolley
#                     wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='enter Trolley number']"))).send_keys(trolly)
#                     logger.info(f"Used trolley is :- {trolly}")
#                     # clicking enter vlaue
#                     try:
#                         wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
#                     except :
#                         logger.critical("Unable to click Enter in trolley insertion")
#                     trolley_list.append(trolly)
#                 except Exception as e:
#                     logger.error(f"Got error in trolley creation and insertion {e}")
#                     raise

#                 #now going to load containers
#                 try:

#                     # get progress vlaue which need to load
#                     try:
#                         progress_value = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Progress']/following-sibling::android.widget.EditText"))).text
#                         loaded, total = progress_value.split("/")
#                         total_to_load = int(total)
#                         loaded = int(loaded)
#                         value = total_to_load - loaded
#                         logger.info(f"Total number of container to load is :- {total_to_load}")
#                     except Exception as e:
#                         logger.error(f"Erro at the time of get number of container to load {e}")
#                         raise

#                     try:
#                         # going to load
#                         while 0 < value:
#                             logger.info(f"going to load contaiiner :- {containers[value -1]}")
#                             # inserting container vlaue
#                             wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@text='container no.']")))
#                             wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='container no.']"))).send_keys(containers[value -1])

#                             loaded_containers.append(containers[value -1])
#                             # clicking enter
#                             # try:
#                             #     wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.TextView[@text='Enter']"))).click()
#                             # except:
#                             #     pass

#                             try:
#                                 ERROR_XPATH = (
#                                     "//android.widget.TextView[string-length(normalize-space(@text)) > 0 and contains(@text,'unknown')]"
#                                 )

#                                 error_el = WebDriverWait(driver, 3).until(
#                                     EC.visibility_of_element_located((By.XPATH, ERROR_XPATH))
#                                 )


#                                 error_text = error_el.get_attribute("text")
#                                 if error_text:
#                                     logger.error(f"Error at the time of container '{containers[value -1]}' insertion :- {error_text}")
#                                     raise RuntimeError(error_text) 
#                             except TimeoutException:
#                                 pass

#                             try:
#                                 wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()
#                             except:
#                                 pass
#                             time.sleep(3)
#                             value = value-1

#                         # clicking end button

#                         try:
#                             progress_value = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Progress']/following-sibling::android.widget.EditText"))).text
#                             loaded, total = progress_value.split("/")
#                             total_to_load = int(total)
#                             loaded = int(loaded)
#                             logger.info(f"Remaining containers in {missioin_value} :- {total_to_load - loaded}")
#                         except Exception as e:
#                             logger.error(f"Erro at the time of get number of container to load {e}")
#                             raise
#                         if loaded==total_to_load:
#                             try:
#                                 wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='End']"))).click()
#                                 logger.info(f"End button clicked")
#                                 time.sleep(5)
#                             except Exception as e:
#                                 logger.error(f"Unable to click end button {e}")
#                                 raise

#                             # getting mission vlaue after clicking end
#                             try:
#                                 missioin_value = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText"))).text
#                             except Exception as e:
#                                 logger.error(f"Unable to get mission number after clicking End button {e}")
#                                 raise
#                         time.sleep(3)
                    
#                     except Exception as e:
#                         logger.error(f"Got error at the time of load container :- {e}")
#                         raise
                
#                 except Exception as e:
#                     logger.info(f"Unable to load container := {e}")
#                     raise


#             if missioin_value not in mission:
#                 #clicking next
#                 wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Next']"))).click()
#                 # getting mission value
#                 missioin_value = wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText"))).text
#             current = missioin_value
        
#         if current == first_mission:
#             logger.info(f"All trolley used in mission distribution are :- {trolley_list}")
#             logger.info("ALL MISSION DISTRIBUTION COMPLETED")

        
#         driver.quit()
#         return trolley_list




from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import WebDriverException
from appium.options.android import UiAutomator2Options

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
    return Android.login()


loaded_containers = []

def distribution(mission, containers):

    driver = Android.login()
    wait = WebDriverWait(driver, 20)

    boxes = containers.copy()
    # loaded_containers = []
    trolley_list = []

    try:
        # click mission
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//android.widget.TextView[@text='Mission']")
        )).click()

        # click distribution
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//android.widget.TextView[@text='Mission distribution']")
        )).click()

        logger.info(f"Going to do mission distribution for :- {mission}")

        missioin_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText")
            )
        ).text

        current = ""
        first_mission = missioin_value

        while first_mission != current:

            if missioin_value in mission:
                logger.info(f"Mission number : {missioin_value} : selected")
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//android.widget.TextView[@text='Enter']")
                )).click()

                location_vlaue = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//android.widget.TextView[@text='Location']/following-sibling::android.widget.EditText")
                    )
                ).text

                containers_list = [
                    box for box, loc in boxes.items()
                    if loc == "19@" + location_vlaue and box not in loaded_containers
                ]

                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@text='confirm location?']")
                )).send_keys(location_vlaue)

                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//android.widget.TextView[@text='Enter']")
                )).click()

                trolley = "03999999123456" + str(random.randint(1000, 9999))
                trolley_list.append(trolley)

                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@text='enter Trolley number']")
                )).send_keys(trolley)
                logger.info(f"using trolley number is :- {trolley}")

                try:
                    wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//android.widget.TextView[@text='Enter']")
                    )).click()
                except:
                    pass

                progress_value = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//android.widget.TextView[@text='Progress']/following-sibling::android.widget.EditText")
                    )
                ).text

                loaded, total = progress_value.split("/")
                value = int(total) - int(loaded)

                while value > 0:
                    logger.info(f"going to load contaiiner :- {containers_list[value - 1]}")

                    wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//android.widget.EditText[@text='container no.']")
                    )).send_keys(containers_list[value - 1])

                    loaded_containers.append(containers_list[value - 1])

                    try:
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//android.widget.TextView[@text='Enter']")
                        )).click()
                    except:
                        pass

                    time.sleep(3)
                    value -= 1

                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//android.widget.TextView[@text='End']")
                )).click()
                logger.info(f"Mission [{missioin_value}] end :")

                time.sleep(5)

                missioin_value = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText")
                    )
                ).text

            if missioin_value not in mission:
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//android.widget.TextView[@text='Next']")
                )).click()

                missioin_value = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//android.widget.TextView[@text='Mission']/following-sibling::android.widget.EditText")
                    )
                ).text

            current = missioin_value

        logger.info(f"All trolley used in mission distribution are :- {trolley_list}")
        return trolley_list

    except Exception as e:
        if is_ui_crash(e):
            logger.error("UI crash detected inside distribution")
            raise
        raise

    finally:
        try:
            driver.quit()
        except:
            pass



class mission:

    def get_boxes(po_number,driver):
        try:
            logger.info("getting Integration controller....")

            wait = WebDriverWait(driver, 20)

            preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[8]/a[1]/span[1]")))
            actions = ActionChains(driver)
            actions.move_to_element(preparation).perform()

            boxes = wait.until(EC.element_to_be_clickable((By.XPATH, "//body/div[@id='root']/div[@id='sessionCheck']/div/nav/ul/li[8]/ul[1]/li[1]/a[1]")))
            actions.move_to_element(boxes).perform()
            boxes.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            po_order = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
            po_order.send_keys(po_number)

            submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            submit.click()
            time.sleep(3)

            data = []

            while True:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".rt-tbody .rt-tr-group"))
                )
                rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")

                for row in rows:
                    cells = row.find_elements(By.CSS_SELECTOR, ".rt-td")

                    if len(cells) > 10:
                        box = cells[3].text.strip()
                        parent_container = cells[8].text.strip()
                        location = cells[10].text.strip()

                        data.append({
                            "Box": box,
                            "Parent Container No": parent_container,
                            "Location": location
                        })

                # pagination
                try:
                    next_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Next']")
                    if next_btn.is_enabled():
                        next_btn.click()
                        time.sleep(2)
                    else:
                        break
                except:
                    break
            #----
            df = pd.DataFrame(data)

            boxes_df = df[
                (
                    df["Parent Container No"].isna() |
                    (df["Parent Container No"].str.strip() == "")
                )
                &
                (df["Box"].notna()) &
                (df["Box"].str.strip() != "")
            ]

            try:
                driver.quit()
            except:
                pass
            result = dict(zip(boxes_df["Box"], boxes_df["Location"]))
            return result
        except:
            logger.error(f"Unable to get boxes")



    def distribution_with_retry(mission, containers, max_retries=8):
        attempt = 0

        while attempt <= max_retries:
            try:
                return distribution(mission, containers)

            except Exception as e:
                if is_ui_crash(e):
                    attempt += 1
                    logger.error(
                        f"UI crash detected. Restarting distribution. "
                        f"Attempt {attempt}/{max_retries}"
                    )
                    time.sleep(5)
                    continue
                raise

        logger.error("Maximum retry limit reached. Stopping execution.")
        exit(1)
        return []

    

    