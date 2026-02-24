import sys
import os
import json
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
import ast
from common_controllers.logger import get_logger 
from common_controllers.poIntegrationMB_controller import poIntegrationMultiLines
from common_controllers.wms_application_login import wms_application_logginPage

logger = get_logger(__name__)
driver = wms_application_logginPage.login()


xml_path = r"C:\\jenkingsProject\\Android_automation\\main\\common_controllers\\documents\\XML\\PO_IN_MB.xml"
po_path = r"C:\\jenkingsProject\\Android_automation\\main\\NormalShippingCycleMB\\reports\\share_data\\PO_number.txt"


def integration_multi_lines():
    """
    Test case for PO Integration with multiple lines.
    Reads only batch numbers from JSON file,
    sets fixed quantities (2 and 3),
    creates XML, saves to file, and integrates into the system.
    """

    try:
        batches_file_path = r"C:\jenkingsProject\Android_automation\main\NormalShippingCycleMB\reports\share_data\batch.txt"
        qty_file_path = r"C:\jenkingsProject\Android_automation\main\NormalShippingCycleMB\reports\share_data\quantity.txt"

        with open(batches_file_path, "r") as f:
            batches = ast.literal_eval(f.read())

        with open(qty_file_path, "r") as f:
            qtys = ast.literal_eval(f.read())

        batch_no_1 = batches[0]
        batch_no_2 = batches[1]
        quantity_1 = qtys[0]
        quantity_2 = qtys[1]

        logger.info(f"Batch 1: {batch_no_1}, Quantity 1: {quantity_1}")
        logger.info(f"Batch 2: {batch_no_2}, Quantity 2: {quantity_2}")

    except Exception:
        logger.exception("Failed to read batch data from created_containers.json")
        return

    logger.info("Getting poIntegrationMultiLines controller .....")

    # Create XML
    xml, po, batch_no_1, batch_no_2, qty_1, qty_2 = poIntegrationMultiLines.xmlCreation(
        batch_no_1=batch_no_1,
        batch_no_2=batch_no_2,
        quantity_1=quantity_1,
        quantity_2=quantity_2
    )

    #  Save/Update XML file
    try:
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml)
        logger.info(f"XML saved successfully at {xml_path}")
    except Exception:
        logger.exception("Failed to save XML file")

    #  Save PO number separately
    try:
        with open(po_path, "w", encoding="utf-8") as f:
            f.write(str(po))
        logger.info(f"PO number saved successfully at {po_path}")
    except Exception:
        logger.exception("Failed to save PO number file")

    # Integrate XML
    poIntegrationMultiLines.Integration(
        driver=driver,
        xml=xml,
        po=po,
        batch_no_1=batch_no_1,
        batch_no_2=batch_no_2,
        qty_1=qty_1,
        qty_2=qty_2
    )

    # Verify integration
    poIntegrationMultiLines.poTest(driver=driver, po=po)


if __name__ == "__main__":
    integration_multi_lines()


