import sys
import os
import ast
import pandas as pd
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.loadTrailler_controller import loadTrailer
from common_controllers.wms_application_login import wms_application_logginPage


logger = get_logger(__name__)

with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycleMB\\reports\\share_data\\RFID.txt", "r") as f:
        rfid = f.read().strip()

with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycleMB\\reports\\share_data\\PO_number.txt", "r") as f:
        po = f.read().strip()
        
driver = wms_application_logginPage.login()
all_boxes = loadTrailer.getBoxes(driver,po)


# driver = test_radiologin()
loadTrailer.LoadTrailer(rfid = rfid,containers=list(all_boxes))