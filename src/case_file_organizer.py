import os
import re
import shutil
import logging
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path
import threading
from queue import Queue
import io

from core.config_manager import ConfigManager
from core.pattern_manager import PatternManager
from gui.progress_window import ProgressWindow
from utils.logger import Logger
from utils.file_utils import FileUtils

class CaseFileOrganizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Case File Organizer")
        self.root.geometry("800x600")
        
        # Initialize managers and utilities
        self.config_manager = ConfigManager()
        self.file_utils = FileUtils()
        self.logger = Logger().get_logger()
        
        # Create GUI
        self.create_gui()
        
        # Initialize variables
        self.processing = False
        self.progress_window = None
        self.processing_queue = Queue()
        
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Directory selection
        ttk.Label(main_frame, text="Select Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dir_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.dir_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_directory).grid(row=0, column=2)
        
        # Pattern selection
        ttk.Label(main_frame, text="Select Pattern:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pattern_var = tk.StringVar()
        self.pattern_combo = ttk.Combobox(main_frame, textvariable=self.pattern_var)
        self.pattern_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        self.update_pattern_list()
        
        # Pattern management buttons
        pattern_frame = ttk.Frame(main_frame)
        pattern_frame.grid(row=1, column=2, sticky=tk.W)
        ttk.Button(pattern_frame, text="Add", command=self.add_pattern).pack(side=tk.LEFT, padx=2)
        ttk.Button(pattern_frame, text="Edit", command=self.edit_pattern).pack(side=tk.LEFT, padx=2)
        ttk.Button(pattern_frame, text="Delete", command=self.delete_pattern).pack(side=tk.LEFT, padx=2)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Create year folders checkbox
        self.create_year_folders = tk.BooleanVar(value=self.config_manager.get_setting('create_year_folders'))
        ttk.Checkbutton(options_frame, text="Create year folders", 
                       variable=self.create_year_folders).grid(row=0, column=0, sticky=tk.W)
        
        # Sort by year checkbox
        self.sort_by_year = tk.BooleanVar(value=self.config_manager.get_setting('sort_by_year'))
        ttk.Checkbutton(options_frame, text="Sort by year", 
                       variable=self.sort_by_year).grid(row=0, column=1, sticky=tk.W)
        
        # Backup before move checkbox
        self.backup_before_move = tk.BooleanVar(value=self.config_manager.get_setting('backup_before_move'))
        ttk.Checkbutton(options_frame, text="Backup before move", 
                       variable=self.backup_before_move).grid(row=0, column=2, sticky=tk.W)
        
        # Fix spaces checkbox
        self.fix_spaces = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Fix spaces in filenames", 
                       variable=self.fix_spaces).grid(row=0, column=3, sticky=tk.W)
        
        # Organize button
        ttk.Button(main_frame, text="Organize Files", 
                  command=self.start_organization).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.set(directory)
            
    def update_pattern_list(self):
        patterns = self.config_manager.get_all_patterns()
        self.pattern_combo['values'] = list(patterns.keys())
        if patterns:
            self.pattern_combo.set(list(patterns.keys())[0])
            
    def add_pattern(self):
        pattern_manager = PatternManager(self.root, self.config_manager)
        pattern_manager.show()
        self.update_pattern_list()
        
    def edit_pattern(self):
        pattern_name = self.pattern_var.get()
        if not pattern_name:
            messagebox.showerror("Error", "Please select a pattern to edit")
            return
            
        pattern_manager = PatternManager(self.root, self.config_manager, pattern_name)
        pattern_manager.show()
        self.update_pattern_list()
        
    def delete_pattern(self):
        pattern_name = self.pattern_var.get()
        if not pattern_name:
            messagebox.showerror("Error", "Please select a pattern to delete")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete pattern '{pattern_name}'?"):
            self.config_manager.delete_pattern(pattern_name)
            self.update_pattern_list()
            
    def start_organization(self):
        if self.processing:
            return
            
        directory = self.dir_path.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return
            
        pattern_name = self.pattern_var.get()
        if not pattern_name:
            messagebox.showerror("Error", "Please select a pattern")
            return
            
        # Save current settings
        self.config_manager.update_setting('create_year_folders', self.create_year_folders.get())
        self.config_manager.update_setting('sort_by_year', self.sort_by_year.get())
        self.config_manager.update_setting('backup_before_move', self.backup_before_move.get())
        
        # Start processing in a separate thread
        self.processing = True
        self.processing_thread = threading.Thread(
            target=self.process_files,
            args=(directory, pattern_name)
        )
        self.processing_thread.start()
        
    def process_files(self, directory, pattern_name):
        try:
            pattern = self.config_manager.get_pattern(pattern_name)
            if not pattern:
                raise ValueError(f"Pattern '{pattern_name}' not found")
                
            # Get list of files
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
            
            # Filter files by pattern
            pattern_files = [f for f in files if re.match(pattern['regex'], f)]
            
            if not pattern_files:
                self.log_message("No files found matching the pattern")
                return
                
            # Create progress window
            self.progress_window = ProgressWindow(self.root, len(pattern_files))
            
            # Process files
            for i, filename in enumerate(pattern_files):
                if self.progress_window.cancel_var.get():
                    break
                    
                try:
                    self.process_single_file(directory, filename, pattern)
                    self.progress_window.update(i + 1, len(pattern_files), 
                                             f"Processing {filename}")
                except Exception as e:
                    self.log_message(f"Error processing {filename}: {str(e)}")
                    
            if not self.progress_window.cancel_var.get():
                self.log_message("File organization completed successfully")
                
        except Exception as e:
            self.log_message(f"Error during file organization: {str(e)}")
        finally:
            self.processing = False
            if self.progress_window:
                self.progress_window.window.destroy()
                
    def process_single_file(self, directory, filename, pattern):
        file_path = os.path.join(directory, filename)
        
        # Create backup if enabled
        if self.backup_before_move.get():
            backup_path = self.file_utils.create_backup(file_path)
            self.log_message(f"Created backup: {backup_path}")
            
        try:
            # Extract information from filename
            match = re.match(pattern['regex'], filename)
            if not match:
                raise ValueError("Filename does not match pattern")
                
            # Get the number and year from the match
            number = match.group(1)
            year = "20" + match.group(2)  # Convert 2-digit year to 4-digit
            
            # Create target directory using the pattern's folder format
            target_dir = pattern['folder_format'].format(
                year=year,
                number=number
            )
            target_dir = os.path.join(directory, target_dir)
            
            # Ensure the target directory exists
            self.file_utils.ensure_directory(target_dir)
            
            # Move file
            target_path = os.path.join(target_dir, filename)
            if self.file_utils.move_file(file_path, target_path):
                self.log_message(f"Moved {filename} to {target_path}")
            else:
                raise ValueError("Failed to move file")
                
        except Exception as e:
            self.log_message(f"Error processing {filename}: {str(e)}")
            raise
            
    def fix_pattern_spaces(self, filename, pattern):
        """Fix spaces in filename according to pattern"""
        self.logger.info(f"Starting space fixing process for pattern '{pattern['name']}'")
        
        # Extract parts from filename
        match = re.match(pattern['regex'], filename)
        if not match:
            return filename
            
        # Get the parts that need space fixing
        parts = match.groups()
        
        # Create new filename with fixed spaces
        new_filename = pattern['folder_format']
        for i, part in enumerate(parts):
            placeholder = f"{{{i}}}"
            if placeholder in new_filename:
                # Remove extra spaces and replace with single space
                fixed_part = ' '.join(part.split())
                new_filename = new_filename.replace(placeholder, fixed_part)
                
        # Add original extension
        _, ext = os.path.splitext(filename)
        new_filename += ext
        
        self.logger.info(f"Fixed spaces in filename: {filename} -> {new_filename}")
        return new_filename
        
    def log_message(self, message):
        self.logger.info(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = CaseFileOrganizer()
    app.run() 