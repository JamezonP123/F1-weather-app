# weather app for F1 circuits
#author Jameson

import openmeteo_requests
import tkinter as tk
from tkinter import ttk
import requests

circuits = {
    "Melbourne": {
        "coords": (-37.8497, 144.968),
        "date": "March 6–8, 2026"
    },
    "Shanghai": {
        "coords": (31.3389, 121.2197),
        "date": "March 13–15, 2026"
    },
    "Suzuka": {
        "coords": (34.8431, 136.5411),
        "date": "March 27–29, 2026"
    },
    "Sakhir": {
        "coords": (26.0325, 50.5106),
        "date": "April 10–12, 2026"
    },
    "Jeddah": {
        "coords": (21.6319, 39.1044),
        "date": "April 17–19, 2026"
    },
    "Miami": {
        "coords": (25.9581, -80.2389),
        "date": "May 1–3, 2026"
    },
    "Montreal": {
        "coords": (45.5067, -73.5263),
        "date": "May 22–24, 2026"
    },
    "Monaco": {
        "coords": (43.7347, 7.4206),
        "date": "June 5–7, 2026"
    },
    "Barcelona-Catalunya": {
        "coords": (41.5700, 2.2610),
        "date": "June 12–14, 2026"
    },
    "Spielberg": {
        "coords": (47.2197, 14.7647),
        "date": "June 26–28, 2026"
    },
    "Silverstone": {
        "coords": (52.0786, -1.0169),
        "date": "July 3–5, 2026"
    },
    "Spa-Francorchamps": {
        "coords": (50.4372, 5.9714),
        "date": "July 17–19, 2026"
    },
    "Budapest": {
        "coords": (47.5789, 19.2486),
        "date": "July 24–26, 2026"
    },
    "Zandvoort": {
        "coords": (52.3889, 4.5400),
        "date": "August 21–23, 2026"
    },
    "Monza": {
        "coords": (45.6194, 9.2811),
        "date": "September 4–6, 2026"
    },
    "Madrid": {
        "coords": (40.4030, -3.6180),
        "date": "September 11–13, 2026"
    },
    "Baku": {
        "coords": (40.3725, 49.8533),
        "date": "September 24–26, 2026"
    },
    "Singapore": {
        "coords": (1.2914, 103.8639),
        "date": "October 9–11, 2026"
    },
    "Austin": {
        "coords": (30.1328, -97.6411),
        "date": "October 23–25, 2026"
    },
    "Mexico City": {
        "coords": (19.4042, -99.0907),
        "date": "October 30–November 1, 2026"
    },
    "Sao Paulo": {
        "coords": (-23.7010, -46.6970),
        "date": "November 6–8, 2026"
    },
    "Las Vegas": {
        "coords": (36.1215, -115.1690),
        "date": "November 19–21, 2026"
    },
    "Lusail": {
        "coords": (25.4868, 51.4543),
        "date": "November 27–29, 2026"
    },
    "Yas Marina": {
        "coords": (24.4672, 54.6031),
        "date": "December 4–6, 2026"
    }
}

# Weather code dictionary
weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm (slight/moderate)",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


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
        code = weather["weathercode"]
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