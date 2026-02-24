

import pandas as pd
import sys
import os
import ast
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.traillerGateAllocation_controller import trailler


logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycleMB\\reports\\share_data\\RFID.txt", "r") as f:
        rfid = f.read().strip()
    logger.info(f"getting trailer identification number from local :- {rfid}")
except:
    logger.exception("getting PO number from local FAILD... ")

trailler.traillerGateAllocation(rfid=rfid)


