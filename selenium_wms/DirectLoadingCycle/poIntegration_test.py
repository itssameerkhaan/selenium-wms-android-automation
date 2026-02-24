import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.poIntegration_controller import poIntegration
from common_controllers.wms_application_login import wms_application_logginPage

driver = wms_application_logginPage.login()
logger = get_logger(__name__)

def integration():

    try:
        with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\batch.txt","r") as f:
            batch_no = f.read().strip()
        logger.info(f"getting batch number from local :- {batch_no}")
    except:
        logger.exception("getting batch number from local FAILD... ")

    try:
        with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\quantity.txt", "r") as f:
            quantity = f.read().strip()
        logger.info(f"getting quantity number from local :- {quantity}")
    except:
        logger.info(f"getting quantity number from local FAILD....")

    logger.info("Getting poIntegration controller .....")


    xml,po,qty,batch=poIntegration.xmlCreation(batch_no=batch_no,quantity=quantity)
    po_num = poIntegration.Integration(driver=driver,xml=xml,po=po,qty=qty,batch_no=batch)
    try:
        logger.info("going to save po number ..")
        with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\PO_number.txt", "w") as f:
            f.write(po)
    except Exception as e:
        logger.error(f"Error in file save of po number {po}")
        raise
    poIntegration.poTest(driver=driver,po=po_num)

integration()

