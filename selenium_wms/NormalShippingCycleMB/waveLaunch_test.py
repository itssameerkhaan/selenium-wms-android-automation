import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.waveLaunch_controller import launch
from common_controllers.wms_application_login import wms_application_logginPage

driver = wms_application_logginPage.login()
logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycleMB\\reports\\share_data\\PO_number.txt", "r") as f:
        po = f.read().strip()
    logger.info(f"getting PO number from local :- {po}")
except:
    logger.exception("getting PO number from local FAILD... ")
    sys.exit(1)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycleMB\\reports\\share_data\\LogicalGate.txt", "r") as f:
        logicalgate = f.read().strip()
    logger.info(f"getting Logical Gate from local :- {logicalgate}")
except:
    logger.exception("getting Logical Gate from local FAILD... ")
    sys.exit(1)


try:
    result = launch.waveLaunch(driver=driver, po=po, logicalgate = logicalgate)
    logger.info(result)
except Exception as e:
    logger.critical(f"Wave Launch Exception: {e}")
    sys.exit(1)
