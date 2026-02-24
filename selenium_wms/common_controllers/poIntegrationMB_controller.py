from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from common_controllers.logger import get_logger 
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
import random

xml_path = r"C:\\jenkingsProject\\Android_automation\\main\\common_controllers\\documents\\XML\\PO_IN_MB.xml"
# po_file_path = r"C:\jenkingsProject\Testing_Main\root_project\root_main\reports\share_data\PO_number.txt"
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


class poIntegrationMultiLines:
    @staticmethod
    def xmlCreation(batch_no_1, batch_no_2, quantity_1, quantity_2):
        try:
            number = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            po = '2324147' + number + '-01'

            po_creation = root.find("PO_CREATION")
            po_creation.set("preparationOrder", po)
            logger.info(f"PO number in xml is :- {po}")

            lines = po_creation.findall(".//PO_LINES/LINE")
            if len(lines) >= 2:
                # line 1
                batch_1 = lines[0].find(".//CHARACTERISTICS/BATCH")
                if batch_1 is not None:
                    batch_1.text = batch_no_1
                qty_1 = lines[0].find(".//QTY_TO_BE_PREP")
                if qty_1 is not None:
                    qty_1.text = str(int(quantity_1) - 1)

                # line 2
                batch_2 = lines[1].find(".//CHARACTERISTICS/BATCH")
                if batch_2 is not None:
                    batch_2.text = batch_no_2
                qty_2 = lines[1].find(".//QTY_TO_BE_PREP")
                if qty_2 is not None:
                    qty_2.text = str(int(quantity_2) - 1)

            # trailer id
            number2 = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            trailer_id = '000000000010214391' + number2
            shipping_trailer = po_creation.find(".//SPEC_PO_SHIPPING_TRAILERS/SPEC_SHIPPING_TRAILER")
            if shipping_trailer is not None:
                shipping_trailer.set("id", trailer_id)

            updated_xml_string = ET.tostring(root, encoding="unicode")
            pretty_xml = xml.dom.minidom.parseString(updated_xml_string).toprettyxml()
            logger.info(f"Updated XML is :- \n {pretty_xml}")
            return updated_xml_string, po, batch_no_1, batch_no_2, int(quantity_1) - 1, int(quantity_2) - 1
        except Exception:
            logger.exception(": XML creation FAILED :")

    def Integration(driver, xml, po, batch_no_1, batch_no_2, qty_1, qty_2):
        try:
            logger.info("getting Integration controller....")
            wait = WebDriverWait(driver, 20)

            Administration = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(Administration).perform()

            file_integration = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[1]/ul/li[8]/a")))
            actions.move_to_element(file_integration).perform()
            file_integration.click()

            neutral_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
            ActionChains(driver).move_to_element(neutral_element).perform()

            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='myid']")))
            if checkbox.is_selected():
                checkbox.click()
                logger.info("Checkbox unchecked .......")

            text_area = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[2]/textarea")))
            text_area.clear()
            text_area.send_keys(xml)
            time.sleep(5)

            int_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/form/div[2]/div/div[3]/div[3]/button")))
            int_button.click()
            logger.info("XML insertion completed")

            success_text = wait.until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='File Integrated Successfully']")))
            if success_text.text:
                logger.info(f"Preparation Order: {po}")
                logger.info(f"Batch numbers: {batch_no_1}, {batch_no_2}")
                logger.info(f"Quantities: {qty_1}, {qty_2}")
                with open(r"C:\\jenkingsProject\\Testing_Main\\root_project\\DirectLoadingWithMB\\reports\\share_data\\PO_number.txt", "w") as f:
                    f.write(po)
                return driver
        except Exception:
            logger.exception(": Unable to integrate XML :")

    def poTest(driver, po):
        try:
            logger.info("getting Integration controller....")
            wait = WebDriverWait(driver, 20)

            preparation = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[8]/a")))
            actions = ActionChains(driver)
            actions.move_to_element(preparation).perform()

            orders = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='sessionCheck']/div[1]/nav/ul/li[8]/ul/li[3]/a")))
            actions.move_to_element(orders).perform()
            orders.click()

            po_order = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='idPrepOrder']")))
            po_order.send_keys(po)

            submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Submit']")))
            submit.click()
            time.sleep(3)

            po_avl= wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='sessionCheck']/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div/div[6]")))
            launchable_test = wait.until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='_Launchable_']")))
            if po_avl.text == str(po) and launchable_test.text == '_Launchable_':
                logger.info(f"Confirm Preparation Order :- {po_avl.text}")
                logger.info(f"Preparation Order Status is :- {launchable_test.text}")
            else:
                logger.error(": FAILED TO GET STATUS AND PREPARATION ORDER :")
        except:
            logger.error(": Unable to find PO in PREPARATION -> ORDER :")

