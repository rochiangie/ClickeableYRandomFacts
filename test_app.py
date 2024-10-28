import unittest
from unittest.mock import patch
from tkinter import Tk, messagebox
import requests
from app import RandomDataApp  # Asegúrate de que el nombre del archivo principal sea correcto

class TestRandomDataApp(unittest.TestCase):
    
    def setUp(self):
        self.root = Tk()
        self.app = RandomDataApp(self.root)
    
    def tearDown(self):
        self.root.destroy()

    def test_initial_click_count(self):
        self.assertEqual(self.app.click_count, 0)

    def test_random_threshold_generation(self):
        threshold = self.app.generate_random_threshold()
        self.assertGreaterEqual(threshold, 3)
        self.assertLessEqual(threshold, 10)

    def test_click_increment(self):
        initial_count = self.app.click_count
        self.app.on_click()
        self.assertEqual(self.app.click_count, initial_count + 1)

    def test_reset_click_count_after_threshold(self):
        self.app.random_threshold = 1
        self.app.on_click()
        self.assertEqual(self.app.click_count, 0)

    @patch('requests.get', side_effect=requests.exceptions.RequestException("Simulated Connection Error"))
    @patch('tkinter.messagebox.showerror')
    def test_show_error_on_api_failure(self, mock_showerror, mock_get):
        self.app.fetch_random_data()
        mock_showerror.assert_called_once_with("Error", "No se pudo obtener el consejo: Simulated Connection Error")

if __name__ == '__main__':
    unittest.main()


