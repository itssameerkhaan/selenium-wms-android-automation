from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
import random
xml_path = r"C:\\jenkingsProject\\Android_automation\\main\\common_controllers\\documents\\XML\\PO_IN.xml"
tree = ET.parse(xml_path)
root = tree.getroot()
logger = get_logger(__name__)

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

options.add_argument("--log-level=3")
options.add_argument("--disable-notifications")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage") 

class poIntegration:
    @staticmethod
    def xmlCreation(batch_no,quantity):
        try:

            number = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            po = '2262768'+number+'-01'

           
            po_creation = root.find("PO_CREATION")
            po_creation.set("preparationOrder", po)
            logger.info(f"PO number is xml is :- {po}")

           
            batch = po_creation.find(".//CHARACTERISTICS/BATCH")
            if batch is not None:
                batch.text = batch_no
                logger.info(f"Batch number is in xml is :- {batch_no}")

            
            qty = po_creation.find(".//PO_LINES/LINE/QTY_TO_BE_PREP")
            if qty is not None:
                qty.text = str(int(quantity)-5)
                logger.info(f"Quantity to be prep :- {int(quantity)-5}")

            
            number2 = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            trailler_id = '000000000078114897'+number2
            shipping_trailer = po_creation.find(".//SPEC_PO_SHIPPING_TRAILERS/SPEC_SHIPPING_TRAILER")
            if shipping_trailer is not None:
                shipping_trailer.set("id", trailler_id)
                logger.info(f"shippint trialler id is :- {trailler_id}")

            # Convert back to an XML string (in proper XML format)
            updated_xml_string = ET.tostring(root, encoding="unicode")
            pretty_xml = xml.dom.minidom.parseString(updated_xml_string).toprettyxml()
            logger.info(f"Updated XML is :- \n {pretty_xml}")
            return updated_xml_string,po,int(quantity)-5,batch_no
        except Exception as e:
            logger.exception(": XML creation FAILED :")
    

    def Integration(driver,xml,po,qty,batch_no):

        try:
            logger.info("getting Integration controller....")

            wait = WebDriverWait(driver, 20)

            Administration = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(Administration).perform()

            file_intigration = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/ul/li[8]/a")))
            actions.move_to_element(file_intigration).perform()
            file_intigration.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='myid']")))


            try:
                if checkbox.is_selected():
                    checkbox.click()
                    logger.info("Checkbox is now unchecked .......")

                    time.sleep(5)
                else:
                    logger.info("Checkbox was already unchecked.....")
            except:
                logger.critical(": Unable to unchake sap posting :")
                exit()
            
            try:
                text_area = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/textarea")))
                text_area.clear()
                text_area.send_keys(xml)
                time.sleep(10)
                try:

                    intigrate_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[3]/div[3]/button")))
                    intigrate_button.click()
                    logger.info("XML inserssion is completed......")
                except:
                    logger.error("XML intigrate button FAILD....")

                successfull_text = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/span")))
                # logger.info("XML intigration status is :- ", successfull_text.text)
                if successfull_text.text:
                    logger.info(f"Preperation Order is :- {po}")
                    logger.info(f"Batch number is :- {batch_no}")
                    logger.info(f"Quantity to be prepare :- {qty}")
                    logger.info(successfull_text.text)
                    return po

            except Exception:
                logger.exception(": Unable to fill xml in text area :")
            
        except Exception:
            logger.exception(": Unable to intigrate XML :")

    
    def poTest(driver,po):

        try:
            logger.info("getting Integration controller....")

            wait = WebDriverWait(driver, 20)

            preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//body[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[8]/a[1]/span[1]")))
            actions = ActionChains(driver)
            actions.move_to_element(preparation).perform()

            orders = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Orders']")))
            actions.move_to_element(orders).perform()
            orders.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            po_order = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
            po_order.send_keys(po)

            submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            submit.click()
            time.sleep(3)

            try:
                # po_avl= wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div/div[6]")))
                launchable_test = wait.until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='_Launchable_']")))
                if launchable_test.text == '_Launchable_':
                    # logger.info(f"Confirm Preparation Order :- {po_avl.text}")
                    logger.info(f"Preparation Ordar Status is :- {launchable_test.text}")
                else:
                    logger.error(": FAILD TO GET STATUS AND PREPERATON ORDER :")
            except:
                logger.error(": Unable to find PO in PREPARATION -> ORDER :")

                
                            
        except:
            logger.info("not")


        

        





