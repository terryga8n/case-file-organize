import unittest
import os
import json
import shutil
from src.core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_config"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_manager = ConfigManager()
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_load_config(self):
        # Test loading default config when no file exists
        config = self.config_manager.load_config()
        self.assertIsNotNone(config)
        self.assertIn("patterns", config)
        self.assertIn("default_settings", config)
        
        # Test loading existing config
        test_config = {
            "patterns": {"test": {"regex": "test"}},
            "default_settings": {"test_setting": True}
        }
        with open(self.config_manager.config_file, 'w') as f:
            json.dump(test_config, f)
            
        config = self.config_manager.load_config()
        self.assertEqual(config["patterns"]["test"]["regex"], "test")
        self.assertTrue(config["default_settings"]["test_setting"])
        
    def test_save_config(self):
        # Test saving config
        test_config = {
            "patterns": {"test": {"regex": "test"}},
            "default_settings": {"test_setting": True}
        }
        self.config_manager.config = test_config
        self.config_manager.save_config()
        
        # Verify saved config
        with open(self.config_manager.config_file, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config, test_config)
        
    def test_get_pattern(self):
        # Test getting existing pattern
        pattern = self.config_manager.get_pattern("ACC")
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern["regex"], r"ACC(\d+)\.(\d+)")
        
        # Test getting non-existent pattern
        pattern = self.config_manager.get_pattern("NONEXISTENT")
        self.assertIsNone(pattern)
        
    def test_get_all_patterns(self):
        patterns = self.config_manager.get_all_patterns()
        self.assertIsNotNone(patterns)
        self.assertIn("ACC", patterns)
        self.assertIn("HREPN", patterns)
        self.assertIn("HRER", patterns)
        
    def test_get_setting(self):
        # Test getting existing setting
        setting = self.config_manager.get_setting("log_level")
        self.assertEqual(setting, "INFO")
        
        # Test getting non-existent setting
        setting = self.config_manager.get_setting("NONEXISTENT")
        self.assertIsNone(setting)
        
    def test_update_pattern(self):
        # Test updating existing pattern
        test_pattern = {
            "regex": r"test(\d+)",
            "folder_format": "test_{number}",
            "description": "Test pattern",
            "sort_by": ["number"]
        }
        self.config_manager.update_pattern("test", test_pattern)
        pattern = self.config_manager.get_pattern("test")
        self.assertEqual(pattern, test_pattern)
        
        # Test adding new pattern
        new_pattern = {
            "regex": r"new(\d+)",
            "folder_format": "new_{number}",
            "description": "New pattern",
            "sort_by": ["number"]
        }
        self.config_manager.update_pattern("new", new_pattern)
        pattern = self.config_manager.get_pattern("new")
        self.assertEqual(pattern, new_pattern)

if __name__ == '__main__':
    unittest.main() 