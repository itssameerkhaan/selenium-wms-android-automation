import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.directMovement_controller import Movement
from common_controllers.wms_application_login import wms_application_logginPage

driver = wms_application_logginPage.login()
logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\batch.txt", "r") as f:
        batch_no = f.read().strip()
    logger.info(f"getting batch number from local :- {batch_no}")
except:
    logger.exception("getting batch number from local FAILD... ")

result = Movement.directMovement(batch_no=batch_no,driver=driver)
logger.info(result)


