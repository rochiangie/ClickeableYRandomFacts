import requests
import tkinter as tk
from tkinter import messagebox
import random

class RandomDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consejos Aleatorios")
        self.click_count = 0
        self.random_threshold = self.generate_random_threshold()
        
        self.label = tk.Label(root, text="Haz clic para recibir un consejo aleatorio.")
        self.label.pack(pady=10)
        
        self.button = tk.Button(root, text="Click", command=self.on_click)
        self.button.pack(pady=10)
        
    def generate_random_threshold(self):
        return random.randint(3, 10)
    
    def on_click(self):
        self.click_count += 1
        if self.click_count >= self.random_threshold:
            self.fetch_random_data()
            self.click_count = 0
            self.random_threshold = self.generate_random_threshold()
    
    def fetch_random_data(self):
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            response.raise_for_status()
            data = response.json()
            advice = data["slip"]["advice"]
            messagebox.showinfo("Consejo Aleatorio", f"Consejo: {advice}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el consejo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomDataApp(root)
    root.mainloop()
