import unittest
import tkinter as tk
from src.gui.progress_window import ProgressWindow

class TestProgressWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.progress_window = ProgressWindow(self.root, 10)
        
    def tearDown(self):
        self.progress_window.window.destroy()
        self.root.destroy()
        
    def test_window_creation(self):
        self.assertIsNotNone(self.progress_window.window)
        self.assertEqual(self.progress_window.window.title(), "Processing Files")
        
    def test_progress_bar(self):
        self.assertIsNotNone(self.progress_window.progress_bar)
        self.assertEqual(self.progress_window.progress_var.get(), 0)
        
    def test_status_label(self):
        self.assertIsNotNone(self.progress_window.status_var)
        self.assertEqual(self.progress_window.status_var.get(), "Processing files...")
        
    def test_cancel_button(self):
        self.assertIsNotNone(self.progress_window.cancel_var)
        self.assertFalse(self.progress_window.cancel_var.get())
        
    def test_update_progress(self):
        self.progress_window.update(5, 10, "Processing file 5")
        self.assertEqual(self.progress_window.progress_var.get(), 5)
        self.assertEqual(self.progress_window.status_var.get(), "Processing file 5 (5/10)")
        
    def test_cancel(self):
        self.progress_window.cancel()
        self.assertTrue(self.progress_window.cancel_var.get())
        
    def test_window_geometry(self):
        self.assertEqual(self.progress_window.window.geometry(), "400x150")
        
    def test_window_transient(self):
        self.assertTrue(self.progress_window.window.transient())
        
    def test_window_grab_set(self):
        self.assertTrue(self.progress_window.window.grab_set())

if __name__ == '__main__':
    unittest.main() 