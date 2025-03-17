import tkinter as tk
from tkinter import ttk, messagebox
import re

class PatternManager:
    def __init__(self, parent, config_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Pattern Manager")
        self.window.geometry("800x600")
        self.config_manager = config_manager
        
        self.setup_gui()
        self.load_patterns()
        
    def setup_gui(self):
        """Setup the pattern management GUI"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pattern list
        list_frame = ttk.LabelFrame(main_frame, text="Available Patterns", padding="5")
        list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create Treeview
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Description"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree['yscrollcommand'] = scrollbar.set
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Pattern", command=self.add_pattern).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Edit Pattern", command=self.edit_pattern).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Pattern", command=self.delete_pattern).grid(row=0, column=2, padx=5)
        
        # Pattern editor frame
        editor_frame = ttk.LabelFrame(main_frame, text="Pattern Editor", padding="5")
        editor_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Pattern name
        ttk.Label(editor_frame, text="Pattern Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Description
        ttk.Label(editor_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.desc_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Regex pattern
        ttk.Label(editor_frame, text="Regex Pattern:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.regex_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.regex_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Folder format
        ttk.Label(editor_frame, text="Folder Format:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.format_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.format_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Save button
        ttk.Button(editor_frame, text="Save Pattern", command=self.save_pattern).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
    def load_patterns(self):
        """Load patterns into the Treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load patterns from config
        patterns = self.config_manager.get_all_patterns()
        for name, data in patterns.items():
            self.tree.insert("", tk.END, values=(name, data["description"]))
    
    def on_select(self, event):
        """Handle pattern selection"""
        selection = self.tree.selection()
        if not selection:
            return
            
        pattern_name = self.tree.item(selection[0])["values"][0]
        pattern_data = self.config_manager.get_pattern(pattern_name)
        
        # Fill editor fields
        self.name_var.set(pattern_name)
        self.desc_var.set(pattern_data["description"])
        self.regex_var.set(pattern_data["regex"])
        self.format_var.set(pattern_data["folder_format"])
    
    def validate_pattern(self):
        """Validate pattern data"""
        name = self.name_var.get().strip()
        desc = self.desc_var.get().strip()
        regex = self.regex_var.get().strip()
        fmt = self.format_var.get().strip()
        
        if not all([name, desc, regex, fmt]):
            messagebox.showerror("Error", "All fields are required!")
            return False
            
        try:
            re.compile(regex)
        except re.error as e:
            messagebox.showerror("Error", f"Invalid regex pattern: {str(e)}")
            return False
            
        # Check for required format placeholders
        if "{number}" not in fmt or "{year}" not in fmt:
            messagebox.showerror("Error", "Folder format must contain {number} and {year} placeholders!")
            return False
            
        return True
    
    def save_pattern(self):
        """Save pattern to configuration"""
        if not self.validate_pattern():
            return
            
        pattern_data = {
            "regex": self.regex_var.get().strip(),
            "folder_format": self.format_var.get().strip(),
            "description": self.desc_var.get().strip(),
            "sort_by": ["number", "year"]
        }
        
        try:
            self.config_manager.update_pattern(self.name_var.get().strip(), pattern_data)
            self.load_patterns()
            messagebox.showinfo("Success", "Pattern saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving pattern: {str(e)}")
    
    def add_pattern(self):
        """Clear editor for new pattern"""
        self.name_var.set("")
        self.desc_var.set("")
        self.regex_var.set("")
        self.format_var.set("")
    
    def edit_pattern(self):
        """Edit selected pattern"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pattern to edit!")
            return
    
    def delete_pattern(self):
        """Delete selected pattern"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pattern to delete!")
            return
            
        pattern_name = self.tree.item(selection[0])["values"][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete pattern '{pattern_name}'?"):
            try:
                del self.config_manager.config["patterns"][pattern_name]
                self.config_manager.save_config()
                self.load_patterns()
                messagebox.showinfo("Success", "Pattern deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting pattern: {str(e)}") 