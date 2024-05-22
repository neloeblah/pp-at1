import unittest
import tkinter as tk

from unittest.mock import patch, Mock

from app import MainApp  


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MainApp(self.root)
    
    def tearDown(self):
        self.root.destroy()
    
    def test_search_query_entry(self):
        query_entry = self.app.left_frame.query_entry
        query_entry.insert(0, 'NBA')
        
        self.assertEqual(query_entry.get(), 'NBA')
    
    def test_country_dropdown(self):
        country_dropdown = self.app.left_frame.country_menu.option_var
        country_dropdown.set('us')
        
        self.assertEqual(country_dropdown.get(), 'us')
    
    def test_language_dropdown(self):
        language_dropdown = self.app.left_frame.language_menu.option_var
        language_dropdown.set('en')
        
        self.assertEqual(language_dropdown.get(), 'en')
    
    def test_category_menu(self):
        for check_var in self.app.left_frame.check_vars:
            check_var.set(False)
            self.assertFalse(check_var.get())

            check_var.set(True)
            self.assertTrue(check_var.get())
    
if __name__ == '__main__':
    unittest.main()