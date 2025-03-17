import unittest
import tkinter as tk
from src.core.config_manager import ConfigManager
from src.core.pattern_manager import PatternManager

class TestPatternManager(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.config_manager = ConfigManager()
        self.pattern_manager = PatternManager(self.root, self.config_manager)
        
    def tearDown(self):
        self.pattern_manager.window.destroy()
        self.root.destroy()
        
    def test_window_creation(self):
        self.assertIsNotNone(self.pattern_manager.window)
        self.assertEqual(self.pattern_manager.window.title(), "Pattern Manager")
        
    def test_pattern_list(self):
        self.assertIsNotNone(self.pattern_manager.pattern_list)
        patterns = self.config_manager.get_all_patterns()
        self.assertEqual(len(self.pattern_manager.pattern_list.get_children()), len(patterns))
        
    def test_pattern_editor(self):
        self.assertIsNotNone(self.pattern_manager.pattern_editor)
        self.assertIsNotNone(self.pattern_manager.name_var)
        self.assertIsNotNone(self.pattern_manager.description_var)
        self.assertIsNotNone(self.pattern_manager.regex_var)
        self.assertIsNotNone(self.pattern_manager.folder_format_var)
        
    def test_add_pattern(self):
        # Set test values
        self.pattern_manager.name_var.set("test_pattern")
        self.pattern_manager.description_var.set("Test pattern description")
        self.pattern_manager.regex_var.set(r"test(\d+)")
        self.pattern_manager.folder_format_var.set("test_{0}")
        
        # Add pattern
        self.pattern_manager.save_pattern()
        
        # Verify pattern was added
        pattern = self.config_manager.get_pattern("test_pattern")
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern['name'], "test_pattern")
        self.assertEqual(pattern['description'], "Test pattern description")
        self.assertEqual(pattern['regex'], r"test(\d+)")
        self.assertEqual(pattern['folder_format'], "test_{0}")
        
    def test_edit_pattern(self):
        # Create test pattern
        test_pattern = {
            'name': 'test_pattern',
            'description': 'Test pattern description',
            'regex': r'test(\d+)',
            'folder_format': 'test_{0}'
        }
        self.config_manager.update_pattern('test_pattern', test_pattern)
        
        # Edit pattern
        self.pattern_manager = PatternManager(self.root, self.config_manager, 'test_pattern')
        self.pattern_manager.name_var.set("test_pattern")
        self.pattern_manager.description_var.set("Updated description")
        self.pattern_manager.regex_var.set(r"test(\d+)")
        self.pattern_manager.folder_format_var.set("test_{0}")
        self.pattern_manager.save_pattern()
        
        # Verify pattern was updated
        pattern = self.config_manager.get_pattern("test_pattern")
        self.assertEqual(pattern['description'], "Updated description")
        
    def test_delete_pattern(self):
        # Create test pattern
        test_pattern = {
            'name': 'test_pattern',
            'description': 'Test pattern description',
            'regex': r'test(\d+)',
            'folder_format': 'test_{0}'
        }
        self.config_manager.update_pattern('test_pattern', test_pattern)
        
        # Delete pattern
        self.pattern_manager.delete_pattern('test_pattern')
        
        # Verify pattern was deleted
        pattern = self.config_manager.get_pattern("test_pattern")
        self.assertIsNone(pattern)
        
    def test_validate_input(self):
        # Test empty name
        self.pattern_manager.name_var.set("")
        self.pattern_manager.description_var.set("Test")
        self.pattern_manager.regex_var.set(r"test(\d+)")
        self.pattern_manager.folder_format_var.set("test_{0}")
        self.assertFalse(self.pattern_manager.validate_input())
        
        # Test empty regex
        self.pattern_manager.name_var.set("test")
        self.pattern_manager.regex_var.set("")
        self.assertFalse(self.pattern_manager.validate_input())
        
        # Test invalid regex
        self.pattern_manager.regex_var.set("invalid[regex")
        self.assertFalse(self.pattern_manager.validate_input())
        
        # Test valid input
        self.pattern_manager.regex_var.set(r"test(\d+)")
        self.assertTrue(self.pattern_manager.validate_input())
        
    def test_pattern_selection(self):
        # Create test pattern
        test_pattern = {
            'name': 'test_pattern',
            'description': 'Test pattern description',
            'regex': r'test(\d+)',
            'folder_format': 'test_{0}'
        }
        self.config_manager.update_pattern('test_pattern', test_pattern)
        
        # Select pattern
        self.pattern_manager.pattern_list.selection_set(self.pattern_manager.pattern_list.get_children()[0])
        self.pattern_manager.on_select()
        
        # Verify editor was populated
        self.assertEqual(self.pattern_manager.name_var.get(), "test_pattern")
        self.assertEqual(self.pattern_manager.description_var.get(), "Test pattern description")
        self.assertEqual(self.pattern_manager.regex_var.get(), r"test(\d+)")
        self.assertEqual(self.pattern_manager.folder_format_var.get(), "test_{0}")

if __name__ == '__main__':
    unittest.main() 