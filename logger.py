import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    def __init__(self, name, log_file='komorebi.log', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        
        # Create file handler and set level to debug
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
        fh = RotatingFileHandler(log_path, maxBytes=1024*1024, backupCount=5)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Create a global logger instance
logger = Logger('komorebi')