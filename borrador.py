import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesario para mostrar imágenes en Tkinter
import random
import io

class RandomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random App")
        self.click_count = 0
        self.random_threshold = self.generate_random_threshold()

        # Etiquetas y botones
        self.label = tk.Label(root, text="Haz clic para recibir una sorpresa aleatoria.")
        self.label.pack(pady=10)

        # Imagen del botón de fondo
        self.button_image = ImageTk.PhotoImage(Image.open("boton.png"))  # Ruta a la imagen del botón
        self.button = tk.Button(root, image=self.button_image, command=self.on_click, bd=0)
        self.button.pack(pady=10)
        
        # Contenedor de imágenes aleatorias
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def generate_random_threshold(self):
        return random.randint(3, 10)

    def on_click(self):
        self.click_count += 1
        if self.click_count >= self.random_threshold:
            self.fetch_random_data()
            self.click_count = 0
            self.random_threshold = self.generate_random_threshold()

    def fetch_random_data(self):
        # Generar consejo aleatorio
        self.get_advice()
        # Generar imagen aleatoria
        self.get_random_image()
        # Obtener chiste
        self.get_joke()
        # Obtener clima en La Plata
        self.get_weather()

    def get_advice(self):
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            response.raise_for_status()
            data = response.json()
            advice = data["slip"]["advice"]
            messagebox.showinfo("Consejo Aleatorio", f"Consejo: {advice}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el consejo: {e}")

    def get_random_image(self):
        try:
            response = requests.get("https://picsum.photos/300")  # Usando Lorem Picsum
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((300, 300))  # Tamaño de la imagen
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Para mantener referencia de la imagen
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener la imagen: {e}")

    def get_joke(self):
        try:
            response = requests.get("https://v2.jokeapi.dev/joke/Any")
            response.raise_for_status()
            data = response.json()
            joke = data["setup"] + " - " + data["delivery"] if "setup" in data else data["joke"]
            messagebox.showinfo("Chiste Aleatorio", f"Chiste: {joke}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el chiste: {e}")

    def get_weather(self):
        try:
            api_key = "8aa90031f4073ef8a1f233dd279c05d4"  # Reemplaza con tu API key de OpenWeatherMap
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=La%20Plata,AR&appid={api_key}&units=metric&lang=es")
            response.raise_for_status()
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            messagebox.showinfo("Clima en La Plata", f"Clima: {weather}, Temp: {temp}°C")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el clima: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomApp(root)
    root.mainloop()
