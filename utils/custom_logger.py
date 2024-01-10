import logging
import os
from logging.handlers import RotatingFileHandler
import uuid

MAX_LOG_SIZE = 10 * 1024 * 1024 # 10 MB
BACKUPCOUNT = 5 # 5 files
LOG_FOLDER = "logs"
LOG_FILE_NAME = "api_log.log"

class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['guid'], msg), kwargs

class CustomLogging:
    """
    Custom logging class to log messages to console and file
    """
    def __init__(self, log_file):
        self.log_file = log_file
        self.file_handler = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d  - %(message)s"
        )

        # Create a console handler and set its level to DEBUG
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        #Rotating file handler which create backup of logs when it reaches to max size
        self.file_handler = RotatingFileHandler(
            self.log_file, maxBytes=MAX_LOG_SIZE, backupCount=BACKUPCOUNT
        )
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(formatter)

        logger.addHandler(self.file_handler)
        adapter = CustomAdapter(logger, {'guid': uuid.uuid4()})
        return adapter
    def newid(self):
        self.logger.extra['guid'] = uuid.uuid4()


os.makedirs(LOG_FOLDER, exist_ok=True)

log_file_path = os.path.join(LOG_FOLDER, LOG_FILE_NAME)

log_obj = CustomLogging(log_file_path)
logger = log_obj.logger
