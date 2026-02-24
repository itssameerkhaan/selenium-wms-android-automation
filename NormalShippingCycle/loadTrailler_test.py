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

# with open(r"C:\jenkingsProject\Testing_Main\root_project\NormalShippingCycle\reports\share_data\Trolley.txt", "r") as f:
#         Trolley = f.read().strip()
# Trolley = ast.literal_eval(Trolley)

with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\RFID.txt", "r") as f:
        rfid = f.read().strip()

# container_table = pd.read_excel("C:\\jenkingsProject\\Testing_Main\\root_project\\NormalShippingCycle\\reports\\tables\\containers_table.xlsx",dtype={'Container No.': str})
# with open(r"C:\\jenkingsProject\\Testing_Main\\root_project\\NormalShippingCycle\\reports\share_data\\RFID.txt", "r") as f:
#         rfid = f.read().strip()

with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\share_data\\PO_number.txt", "r") as f:
        po = f.read().strip()
# containers = container_table['Container No.'][container_table['Parent Container'].notna()]
# loadTrailer.LoadTrailer(driver=driver,rfid = rfid,containers=list(containers))
driver = wms_application_logginPage.login()
all_boxes = loadTrailer.getBoxes(driver,po)


# driver = test_radiologin()
loadTrailer.LoadTrailer(rfid = rfid,containers=list(all_boxes))