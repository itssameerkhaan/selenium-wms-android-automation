import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.traillerRelease_controller import Trailer

logger = get_logger(__name__)

try:
    with open(r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycle\\reports\\share_data\\RFID.txt", "r") as f:
        rfid = f.read().strip()
    logger.info(f"getting RFID number from local :- {rfid}")
except:
    logger.exception("getting rfid number from local FAILD... ")

Trailer.trailerRelease(rfid=rfid)


