import sys
import os
import pandas as pd
from tabulate import tabulate
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from common_controllers.logger import get_logger 
from common_controllers.containerCreation_controller import create_container
from common_controllers.getContainerDetails_controller import getContainer


logger = get_logger(__name__)
def ContainerCreation():
    logger.info("I am in container creation mode, THANKYOU ...")
    try :
        i=1
        batches = []
        quantity = []
        while i<=2:
            batch_no,qty_no = create_container.Create()
            batches.append(batch_no)
            quantity.append(qty_no)
            i=i+1
        with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycleMB\\reports\\share_data\\batch.txt", "w") as f:
            f.write(str(batches))
        with open(r"C:\\jenkingsProject\\Android_automation\\main\\DirectLoadingCycleMB\\reports\\share_data\\quantity.txt", "w") as f:
            f.write(str(quantity))
        logger.info("getting some sample of containers.....")
        for index,batche in enumerate(batches):
            Main_df = getContainer.get(batch_no=batche)
            path = fr"C:\jenkingsProject\Android_automation\main\DirectLoadingCycleMB\reports\tables\containers_{index}.xlsx"
            Main_df.to_excel(path, index=False)
            pd.set_option("display.max_columns", None)       
            pd.set_option("display.max_rows", None)         
            pd.set_option("display.width", None)             
            pd.set_option("display.max_colwidth", None)
            logger.info(f"Sample of Contianers is \n")
            print(tabulate(Main_df.head(), headers='keys', tablefmt='grid', showindex=False))
    except:
        logger.critical("Faild in getting containerCreation_controller")
        raise

ContainerCreation()




