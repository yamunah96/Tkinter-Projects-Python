import tkinter as tk
from tkinter import ttk
import requests
import random
import datetime

# ========== WEATHER CONFIG ==========
API_KEY = "ebd355a4af20d585cc679300add6c2fc"  # 🔑 Replace with your OpenWeatherMap API key
COUNTRIES = ["India", "USA", "UK", "Canada", "Australia", "Japan"]

# ========== FUNCTIONS ==========

# Joke API
def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        resp = requests.get(url)
        data = resp.json()
        setup, punchline = data["setup"], data["punchline"]
        joke_text.set(f"{setup}\n\n{punchline}")
    except Exception:
        joke_text.set("⚠️ Couldn’t fetch joke. Check internet connection.")

# Quote API
def get_quote():
    try:
        url = "https://api.quotable.io/random"
        resp = requests.get(url)
        data = resp.json()
        text, author = data["content"], data["author"]
        quote_text.set(f"“{text}”\n\n— {author}")
    except Exception:
        quote_text.set("⚠️ Couldn’t fetch quote. Try again later.")

# Weather API
def get_weather():
    city = city_entry.get()
    if not city.strip():
        weather_text.set("⚠️ Please enter a city name.")
        return
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        # https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
        response = requests.get(url)
        data = response.json()
        print(data)
        if data.get("cod") != 200:
            weather_text.set("❌ City not found. Try again.")
            return

        # Extract details
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        weather = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]

        # Weather icon mapping
        if "cloud" in weather.lower():
            icon = "⛅"
        elif "rain" in weather.lower():
            icon = "🌧️"
        elif "clear" in weather.lower():
            icon = "☀️"
        elif "snow" in weather.lower():
            icon = "❄️"
        else:
            icon = "🌍"

        result = (
            f"{icon} City: {city.title()}\n"
            f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"⬆️ Max: {temp_max}°C | ⬇️ Min: {temp_min}°C\n"
            f"☁️ Condition: {weather}\n"
            f"💧 Humidity: {humidity}%"
        )

        weather_text.set(result)

        # # Save search history
        # with open("weather_history.txt", "a") as f:
        #     f.write(f"[{datetime.datetime.now()}] {result}\n\n")

    except Exception as e:
        weather_text.set("⚠️ Error fetching weather data.\nCheck internet connection.")

# ========== MAIN APP ==========
root = tk.Tk()
root.title("Daily Hub: Jokes, Quotes & Weather 😂✨🌦️")
root.geometry("700x500")

# # Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- JOKE TAB ---
joke_tab = tk.Frame(notebook)
notebook.add(joke_tab, text="😂 Jokes")

tk.Label(joke_tab, text="Need a laugh? Click below!", font=("Arial", 14)).pack(pady=10)
tk.Button(joke_tab, text="Get Joke", command=get_joke, font=("Arial", 12, "bold")).pack(pady=10)

joke_text = tk.StringVar()
tk.Label(joke_tab, textvariable=joke_text, wraplength=650, justify="center", font=("Arial", 12)).pack(pady=20)

# --- QUOTE TAB ---
quote_tab = tk.Frame(notebook)
notebook.add(quote_tab, text="✨ Quotes")

tk.Label(quote_tab, text="Get inspired! Click below!", font=("Arial", 14)).pack(pady=10)
tk.Button(quote_tab, text="Get Quote", command=get_quote, font=("Arial", 12, "bold")).pack(pady=10)

quote_text = tk.StringVar()
tk.Label(quote_tab, textvariable=quote_text, wraplength=650, justify="center", font=("Arial", 12)).pack(pady=20)

# --- WEATHER TAB ---
weather_tab = tk.Frame(notebook)
notebook.add(weather_tab, text="🌦️ Weather")

tk.Label(weather_tab, text="Enter City:", font=("Arial", 12)).pack(pady=5)
city_entry = tk.Entry(weather_tab, font=("Arial", 12), justify="center")
city_entry.pack(pady=5)



tk.Button(weather_tab, text="Get Weather", command=get_weather, font=("Arial", 12, "bold")).pack(pady=10)

weather_text = tk.StringVar()
tk.Label(weather_tab, textvariable=weather_text, font=("Arial", 12), justify="left", wraplength=650, padx=10, pady=10).pack()

# Run App
root.mainloop()
