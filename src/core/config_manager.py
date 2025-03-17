import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_file = "file_patterns.json"
        self.default_config = {
            "patterns": {
                "ACC": {
                    "regex": r"ACC(\d+)\.(\d{2})",
                    "folder_format": "ACC/{year}/ACC{number}.{year}",
                    "description": "Accident case files (format: ACC134.23)",
                    "sort_by": ["number", "year"]
                },
                "HREPN": {
                    "regex": r"HREPN(\d+)\.(\d{2})",
                    "folder_format": "HREPN/{year}/HREPN{number}.{year}",
                    "description": "Human rights enforcement case files (format: HREPN134.23)",
                    "sort_by": ["number", "year"]
                },
                "HRER": {
                    "regex": r"HRER(\d+)\.(\d{2})",
                    "folder_format": "HRER/{year}/HRER{number}.{year}",
                    "description": "Human rights enforcement report files (format: HRER134.23)",
                    "sort_by": ["number", "year"]
                }
            },
            "settings": {
                "create_year_folders": True,
                "sort_by_year": True,
                "backup_before_move": True
            }
        }
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_config
        return self.default_config
        
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def get_all_patterns(self):
        """Get all patterns"""
        return self.config.get("patterns", {})
        
    def get_pattern(self, name):
        """Get a specific pattern by name"""
        return self.config.get("patterns", {}).get(name)
        
    def update_pattern(self, name, pattern_data):
        """Update or add a pattern"""
        if "patterns" not in self.config:
            self.config["patterns"] = {}
        self.config["patterns"][name] = pattern_data
        self.save_config()
        
    def delete_pattern(self, name):
        """Delete a pattern"""
        if name in self.config.get("patterns", {}):
            del self.config["patterns"][name]
            self.save_config()
            
    def get_setting(self, name):
        """Get a setting value"""
        return self.config.get("settings", {}).get(name, False)
        
    def update_setting(self, name, value):
        """Update a setting value"""
        if "settings" not in self.config:
            self.config["settings"] = {}
        self.config["settings"][name] = value
        self.save_config() 