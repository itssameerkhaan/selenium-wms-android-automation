import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.traillerAssociation_controller import Trailler



logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\PO_number.txt", "r") as f:
        po_number = f.read().strip()
    logger.info(f"getting PO number from local :- {po_number}")
except:
    logger.exception("getting PO number from local FAILD... ")

rfid = Trailler.traillerAssociation(po_number=po_number)
with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycle\\reports\\share_data\\RFID.txt", "w") as f:
    f.write(rfid)


