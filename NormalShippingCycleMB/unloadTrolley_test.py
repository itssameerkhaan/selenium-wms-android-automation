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
from common_controllers.getContainerDetails_controller import getContainer
from common_controllers.missionDistribution_controller import mission
from common_controllers.unloadTrolley_controller import unload

logger = get_logger(__name__)

# Load trolley list and container table
with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycleMB\\reports\\share_data\\Trolley_list.txt", "r") as f:
    Trolley = f.read().strip()
Trolley = ast.literal_eval(Trolley)

# container_table = pd.read_excel(
#     "C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycleMB\\reports\\tables\\containers_table.xlsx",
#     dtype={'Container No.': str}
# )
container_table = []
# def test_unloadTrolley(troll, container_table,index,driver):
#     logger = get_logger(__name__)
#     result,driver = unload.Trolley(troll=troll, container_table=container_table,index=index, driver=driver)
#     return result


# Run for all trolleys
logger = get_logger(__name__)
all_results = []
driver = None
for index,troll in enumerate(Trolley):
    # test_unloadTrolley(troll=troll, container_table=container_table, index=index, driver=driver)
    result, driver = unload.trolley_with_retry(troll=troll, container_table=container_table,index=index, driver=driver)
    all_results.append(troll)

#  Success message after all trolleys are unloaded
if len(all_results) == len(Trolley):
    logger = get_logger(__name__)
    logger.info(f"All trolly is unloaded now :- {all_results}")
else:
        logger = get_logger(__name__)
        logger.error("Some trolly is not unloaded")