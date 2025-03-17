import unittest
import os
import shutil
import tkinter as tk
from src.case_file_organizer import CaseFileOrganizer

class TestCaseFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = CaseFileOrganizer()
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test files
        self.create_test_files()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        self.app.root.destroy()
        self.root.destroy()
        
    def create_test_files(self):
        # Create test files with different patterns
        test_files = [
            "ACC1234-5678-9012.pdf",
            "ACC2345-6789-0123.pdf",
            "HREPN1234-5678-9012.pdf",
            "HREPN2345-6789-0123.pdf",
            "HRER1234-5678-9012.pdf",
            "HRER2345-6789-0123.pdf",
            "test_file.txt"  # Non-matching file
        ]
        
        for filename in test_files:
            with open(os.path.join(self.test_dir, filename), 'w') as f:
                f.write("test content")
                
    def test_initialization(self):
        self.assertIsNotNone(self.app.root)
        self.assertIsNotNone(self.app.config_manager)
        self.assertIsNotNone(self.app.file_utils)
        self.assertIsNotNone(self.app.logger)
        
    def test_directory_selection(self):
        self.app.dir_path.set(self.test_dir)
        self.assertEqual(self.app.dir_path.get(), self.test_dir)
        
    def test_pattern_selection(self):
        # Test selecting different patterns
        patterns = self.app.config_manager.get_all_patterns()
        for pattern_name in patterns:
            self.app.pattern_var.set(pattern_name)
            self.assertEqual(self.app.pattern_var.get(), pattern_name)
            
    def test_file_organization(self):
        # Set up test conditions
        self.app.dir_path.set(self.test_dir)
        self.app.pattern_var.set("ACC")
        self.app.create_year_folders.set(True)
        self.app.sort_by_year.set(True)
        self.app.backup_before_move.set(True)
        self.app.fix_spaces.set(True)
        
        # Start organization
        self.app.start_organization()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Verify organization
        acc_dir = os.path.join(self.test_dir, "ACC")
        self.assertTrue(os.path.exists(acc_dir))
        
        # Check if files were organized
        organized_files = []
        for root, _, files in os.walk(acc_dir):
            organized_files.extend(files)
            
        self.assertEqual(len(organized_files), 2)  # Only ACC files
        
    def test_backup_creation(self):
        # Set up test conditions
        self.app.dir_path.set(self.test_dir)
        self.app.pattern_var.set("ACC")
        self.app.backup_before_move.set(True)
        
        # Start organization
        self.app.start_organization()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Check for backup files
        backup_files = [f for f in os.listdir(self.test_dir) if f.endswith('.bak')]
        self.assertEqual(len(backup_files), 2)  # Only ACC files
        
    def test_year_organization(self):
        # Set up test conditions
        self.app.dir_path.set(self.test_dir)
        self.app.pattern_var.set("ACC")
        self.app.create_year_folders.set(True)
        
        # Start organization
        self.app.start_organization()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Check year folders
        acc_dir = os.path.join(self.test_dir, "ACC")
        year_dirs = [d for d in os.listdir(acc_dir) if os.path.isdir(os.path.join(acc_dir, d))]
        self.assertTrue(len(year_dirs) > 0)
        
    def test_space_fixing(self):
        # Create a file with spaces
        spaced_file = os.path.join(self.test_dir, "ACC 1234-5678-9012.pdf")
        with open(spaced_file, 'w') as f:
            f.write("test content")
            
        # Set up test conditions
        self.app.dir_path.set(self.test_dir)
        self.app.pattern_var.set("ACC")
        self.app.fix_spaces.set(True)
        
        # Start organization
        self.app.start_organization()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Check if spaces were fixed
        acc_dir = os.path.join(self.test_dir, "ACC")
        organized_files = []
        for root, _, files in os.walk(acc_dir):
            organized_files.extend(files)
            
        self.assertTrue(any("ACC1234-5678-9012.pdf" in f for f in organized_files))
        
    def test_error_handling(self):
        # Test with invalid directory
        self.app.dir_path.set("invalid_directory")
        self.app.pattern_var.set("ACC")
        
        # Start organization
        self.app.start_organization()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Check log for error message
        log_files = [f for f in os.listdir('logs') if f.startswith('organizer_')]
        latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join('logs', x)))
        
        with open(os.path.join('logs', latest_log), 'r') as f:
            content = f.read()
        self.assertIn("Error", content)
        
    def test_cancellation(self):
        # Set up test conditions
        self.app.dir_path.set(self.test_dir)
        self.app.pattern_var.set("ACC")
        
        # Start organization
        self.app.start_organization()
        
        # Cancel operation
        self.app.progress_window.cancel()
        
        # Wait for processing to complete
        self.app.processing_thread.join()
        
        # Verify cancellation
        acc_dir = os.path.join(self.test_dir, "ACC")
        self.assertFalse(os.path.exists(acc_dir))

if __name__ == '__main__':
    unittest.main() 