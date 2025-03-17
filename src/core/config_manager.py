import os
import json

class ConfigManager:
    def __init__(self):
        # Get the directory where the script is located
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_file = os.path.join(self.base_dir, "file_patterns.json")
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.get_default_config()
        
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def get_default_config(self):
        """Get default configuration"""
        return {
            "patterns": {
                "ACC": {
                    "regex": r"ACC(\d+)\.(\d+)",
                    "folder_format": "ACC{number}.{year}",
                    "description": "Accident case files",
                    "sort_by": ["number", "year"]
                },
                "HREPN": {
                    "regex": r"HREPN(\d+)\.(\d+)",
                    "folder_format": "HREPN{number}.{year}",
                    "description": "Human rights enforcement case files",
                    "sort_by": ["number", "year"]
                },
                "HRER": {
                    "regex": r"HRER(\d+)\.(\d+)",
                    "folder_format": "HRER{number}.{year}",
                    "description": "Human rights enforcement report files",
                    "sort_by": ["number", "year"]
                }
            },
            "default_settings": {
                "log_level": "INFO",
                "create_year_folders": True,
                "sort_by_year": True,
                "backup_before_move": True
            }
        }
        
    def get_pattern(self, pattern_name):
        """Get pattern configuration by name"""
        return self.config["patterns"].get(pattern_name)
        
    def get_all_patterns(self):
        """Get all pattern configurations"""
        return self.config["patterns"]
        
    def get_setting(self, setting_name):
        """Get setting value by name"""
        return self.config["default_settings"].get(setting_name)
        
    def update_pattern(self, pattern_name, pattern_data):
        """Update or add pattern configuration"""
        self.config["patterns"][pattern_name] = pattern_data
        self.save_config() 