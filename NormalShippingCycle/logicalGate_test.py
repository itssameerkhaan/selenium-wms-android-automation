import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.logicalGate_controller import LogicalGate
from common_controllers.wms_application_login import wms_application_logginPage

driver = wms_application_logginPage.login()
logger = get_logger(__name__)


logicalgate_value = LogicalGate.selectGate(driver=driver)
if logicalgate_value:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\LogicalGate.txt", "w") as f:
        f.write(logicalgate_value)
else:
    logger.error(": Unable to store Logical Gate :")

