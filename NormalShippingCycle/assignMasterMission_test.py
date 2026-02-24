import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.wms_application_login import wms_application_logginPage
from common_controllers.assignMasterMission_controller import assignMaster


driver = wms_application_logginPage.login()
logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\PO_number.txt", "r") as f:
        po = f.read().strip()
    logger.info(f"getting PO number from local :- {po}")
except:
    logger.exception("getting PO number from local FAILD... ")
    sys.exit(1)


df = assignMaster.assignmission(driver=driver,po=po)
path = fr"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\tables\\mission_table.xlsx"
logger.info("Creating Mission Table......")
df.to_excel(path, index=False)

