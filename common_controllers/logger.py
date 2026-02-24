import logging
import os
import shutil
import datetime


def get_logger(name=__name__):
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'execution.log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# def backup_log_file():
#     log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'logs', 'execution.log')

#     if os.path.exists(log_file):
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#         backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'logs', 'backup')
#         os.makedirs(backup_dir, exist_ok=True)

#         backup_file = os.path.join(backup_dir, f'execution_{timestamp}.log')
#         shutil.copy(log_file, backup_file)
#         print(f"Backup created at: {backup_file}")
#     else:
#         print("Log file does not exist.")
# backup_log_file()
