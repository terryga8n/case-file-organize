import tkinter as tk
from tkinter import ttk

class ProgressWindow:
    def __init__(self, parent, total_files):
        self.window = tk.Toplevel(parent)
        self.window.title("Processing Files")
        self.window.geometry("400x150")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.window, 
            variable=self.progress_var,
            maximum=total_files
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_var = tk.StringVar(value="Processing files...")
        ttk.Label(self.window, textvariable=self.status_var).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Cancel button
        self.cancel_var = tk.BooleanVar(value=False)
        ttk.Button(self.window, text="Cancel", command=self.cancel).grid(row=2, column=0, columnspan=2, pady=10)
        
    def update(self, current, total, status):
        self.progress_var.set(current)
        self.status_var.set(f"{status} ({current}/{total})")
        self.window.update()
        
    def cancel(self):
        self.cancel_var.set(True)
        self.window.destroy() 