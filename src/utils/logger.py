import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger('CaseFileOrganizer')
        self.logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Create file handler
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(f'logs/organizer_{timestamp}.log')
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def get_logger(self):
        return self.logger 