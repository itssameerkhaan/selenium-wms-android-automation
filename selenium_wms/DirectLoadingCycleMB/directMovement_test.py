import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
import ast
from common_controllers.logger import get_logger 
from common_controllers.directMovement_controller import Movement
from common_controllers.wms_application_login import wms_application_logginPage

logger = get_logger(__name__)

try:
    # with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\batch.txt", "r") as f:
    #     batch_no = f.read().strip()

    file_path = r"C:\jenkingsProject\Android_automation\main\DirectLoadingCycleMB\reports\share_data\batch.txt"

    with open(file_path, "r") as f:
        batches = ast.literal_eval(f.read())

    logger.info(f"getting batch number from local :- {batches}")
except:
    logger.exception("getting batch number from local FAILD... ")
    raise

for batch_no in batches:
    driver = wms_application_logginPage.login()
    result = Movement.directMovement(batch_no=batch_no,driver=driver)
    logger.info(result)


