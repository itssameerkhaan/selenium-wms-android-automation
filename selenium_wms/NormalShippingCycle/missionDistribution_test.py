import pandas as pd
import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.getContainerDetails_controller import getContainer
from common_controllers.missionDistribution_controller import mission
from common_controllers.wms_application_login import wms_application_logginPage

logger = get_logger(__name__)



# def update_container_table():
#     driver = wms_application_logginPage.login()
#     with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\batch.txt", "r") as f:
#         batch_no = f.read().strip()
#     # print("driver is accessible form containerCreation_test :- ",driver.title)
#     Main_df = getContainer.get(driver=driver,batch_no=batch_no)
#     path = r"C:\jenkingsProject\Android_automation\main\NormalShippingCycle\reports\tables\containers_table.xlsx"
#     Main_df.to_excel(path, index=False)
#     pd.set_option("display.max_columns", None)       
#     pd.set_option("display.max_rows", None)         
#     pd.set_option("display.width", None)             
#     pd.set_option("display.max_colwidth", None)

#     return "Updated"

# getting mission table
try:
    path = fr"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\tables\\mission_table.xlsx"
    mission_table = pd.read_excel(path).reset_index()
    mission_no = [str(value) for value in mission_table['Mission No']]
    logger.info(f"Mission number for mission distributin :- {mission_no}")
except Exception as e:
    logger.error(f"Unable to get mission vlaue from local")
    raise




with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\PO_number.txt", "r") as f:
    po_number = f.read().strip()
#getting boxes by po
driver = wms_application_logginPage.login()
try:
    boxes = mission.get_boxes(po_number=po_number,driver=driver)
except Exception as e:
    logger.error(f"Unable to get boxes :- {e}")
    raise
trolley_list = mission.distribution(mission=mission_no,containers=boxes)
if len(trolley_list) == 0:
    logger.info(f"All Mission is already loaded")
else:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\Trolley_list.txt", "w") as f:
        f.write(str(trolley_list))

