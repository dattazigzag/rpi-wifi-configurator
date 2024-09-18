import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
import shutil

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.initial_backup()

    def initial_backup(self):
        if os.path.exists(self.baseFilename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(os.path.dirname(self.baseFilename), "logs")
            os.makedirs(backup_dir, exist_ok=True)
            backup_file = os.path.join(backup_dir, f"log_{timestamp}.log")
            shutil.copy2(self.baseFilename, backup_file)
            os.remove(self.baseFilename)

class Logger:
    def __init__(self, name, log_file='komorebi.log', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # File handler (rotates every 24 hours)
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
        fh = CustomTimedRotatingFileHandler(log_path, when="D", interval=1, backupCount=30)
        fh.setLevel(level)
        fh.setFormatter(formatter)
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