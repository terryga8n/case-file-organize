import os
import shutil
from pathlib import Path
import re
from datetime import datetime

class FileUtils:
    @staticmethod
    def get_file_year(file_path):
        """Extract year from file name or modification time"""
        # Try to get year from filename first
        filename = os.path.basename(file_path)
        year_match = re.search(r'20\d{2}', filename)
        if year_match:
            return year_match.group()
            
        # If no year in filename, use file modification time
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y')
        
    @staticmethod
    def create_backup(file_path):
        """Create a backup of the file"""
        backup_path = f"{file_path}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
        
    @staticmethod
    def restore_backup(backup_path):
        """Restore a file from backup"""
        original_path = backup_path[:-4]  # Remove .bak extension
        shutil.copy2(backup_path, original_path)
        
    @staticmethod
    def move_file(src, dst):
        """Move a file with proper error handling"""
        try:
            shutil.move(src, dst)
            return True
        except Exception as e:
            return False
            
    @staticmethod
    def ensure_directory(path):
        """Ensure directory exists, create if it doesn't"""
        os.makedirs(path, exist_ok=True)
        
    @staticmethod
    def get_file_info(file_path):
        """Get file information including size and modification time"""
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'mtime': datetime.fromtimestamp(stat.st_mtime),
            'ctime': datetime.fromtimestamp(stat.st_ctime)
        }
        
    @staticmethod
    def is_valid_filename(filename):
        """Check if filename is valid for Windows"""
        invalid_chars = '<>:"/\\|?*'
        return not any(char in filename for char in invalid_chars) 