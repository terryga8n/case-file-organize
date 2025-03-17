import unittest
import os
import logging
import shutil
from datetime import datetime
from src.utils.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_logs"
        os.makedirs(self.test_dir, exist_ok=True)
        self.logger = Logger(log_level=logging.DEBUG)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        # Clean up logs directory
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        if os.path.exists(logs_dir):
            shutil.rmtree(logs_dir)
        
    def test_logger_creation(self):
        self.assertIsInstance(self.logger.get_logger(), logging.Logger)
        self.assertEqual(self.logger.get_logger().level, logging.DEBUG)
        
    def test_log_directory_creation(self):
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        self.assertTrue(os.path.exists(logs_dir))
        
    def test_log_file_creation(self):
        logger = self.logger.get_logger()
        logger.info("Test log message")
        
        # Check if log file was created
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('organizer_')]
        self.assertTrue(len(log_files) > 0)
        
        # Check log content
        latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
        with open(os.path.join(logs_dir, latest_log), 'r') as f:
            content = f.read()
        self.assertIn("Test log message", content)
        
    def test_log_levels(self):
        logger = self.logger.get_logger()
        
        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Check if all messages were logged
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('organizer_')]
        latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
        
        with open(os.path.join(logs_dir, latest_log), 'r') as f:
            content = f.read()
            
        self.assertIn("Debug message", content)
        self.assertIn("Info message", content)
        self.assertIn("Warning message", content)
        self.assertIn("Error message", content)
        
    def test_log_format(self):
        logger = self.logger.get_logger()
        logger.info("Test message")
        
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('organizer_')]
        latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
        
        with open(os.path.join(logs_dir, latest_log), 'r') as f:
            content = f.read()
            
        # Check log format
        self.assertRegex(content, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - INFO - Test message')
        
    def test_multiple_handlers(self):
        logger = self.logger.get_logger()
        self.assertEqual(len(logger.handlers), 2)  # File and console handlers
        
    def test_log_rotation(self):
        # Create multiple log files
        for i in range(3):
            logger = Logger(log_level=logging.DEBUG)
            logger.get_logger().info(f"Test message {i}")
            
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('organizer_')]
        self.assertEqual(len(log_files), 3)

if __name__ == '__main__':
    unittest.main() 