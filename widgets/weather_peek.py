"""WeatherPeek - Current weather (compact taskbar mode)."""
import threading
import tkinter as tk
try:
    import requests
except ImportError:
    requests = None

from base import BaseWidget


class WeatherPeek(BaseWidget):
    NAME = "WeatherPeek"
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 70
    UPDATE_INTERVAL = 3600000
    DOCK_TO_BAR = True

    def _build(self):
        self.city = ""
        try:
            from base import load_config
            self.city = load_config().get("weather_city", "")
        except:
            pass

        f = ("Segoe UI", 8)
        self.weather_l = tk.Label(self.win, text="🌤 --°C", bg=self.BG_COLOR, fg=self.FG_COLOR, font=f)
        self.weather_l.pack(side=tk.LEFT, padx=2)

    def _update(self):
        if not requests:
            self.weather_l.config(text="🌤 no requests")
            return
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            resp = requests.get(f"https://wttr.in/{self.city}?format=j1", timeout=10)
            data = resp.json()
            c = data["current_condition"][0]
            temp = c["temp_C"]
            desc = c["weatherDesc"][0]["value"]
            self.win.after(0, lambda: self.weather_l.config(text=f"🌤 {temp}°C {desc}"))
        except:
            self.win.after(0, lambda: self.weather_l.config(text="🌤 --"))
