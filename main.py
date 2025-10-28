# weather app for F1 circuits
#author Jameson

import json
import tkinter as tk
from tkinter import ttk
import requests

#load circuits from json file
with open("circuits.json", "r") as f:
    circuits = json.load(f)

# Note: keys are strings, so when looking up:
with open("weathercodes.json", "r") as w:
    weather_descriptions = json.load(w)

def get_weather(circuit_name):
    if circuit_name not in circuits:
        return "Circuit not found"

    lat, lon = circuits[circuit_name]["coords"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    date = circuits[circuit_name]["date"]

    response = requests.get(url)
    data = response.json()

    if "current_weather" in data:
        weather = data["current_weather"]
        temperature = weather["temperature"]
        wind_speed = weather["windspeed"]
        code = str(weather["weathercode"])  # convert to string for JSON keys
        description = weather_descriptions.get(code, f"Unknown (code {code})")
        return (
            f"🏁 {circuit_name} Grand Prix\n"
            f"📅 {date}\n"
            f"🌡️ Temperature: {temperature}°C\n"
            f"💨 Wind Speed: {wind_speed} km/h\n"
            f"☁️ Conditions: {description}")
    else:
        return "Weather not found"


# --- GUI setup ---
root = tk.Tk()
root.title("F1 Circuit Weather")

root.geometry("400x350")

# Dropdown for circuits
circuit_var = tk.StringVar()
circuit_dropdown = ttk.Combobox(root, textvariable=circuit_var)
circuit_dropdown['values'] = list(circuits.keys())
circuit_dropdown.grid(row=0, column=0, padx=10, pady=10)

# Weather display area
weather_text = tk.Text(root, height=12, width=45)
weather_text.grid(row=2, column=0, padx=10, pady=10)

# Button to get weather
def show_weather():
    circuit_name = circuit_var.get()
    if not circuit_name:
        weather_text.delete(1.0, tk.END)
        weather_text.insert(tk.END, "Please select a circuit.")
        return

    weather_info = get_weather(circuit_name)
    weather_text.delete(1.0, tk.END)
    weather_text.insert(tk.END, weather_info)

get_weather_button = tk.Button(root, text="Show Weather", command=show_weather)
get_weather_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()