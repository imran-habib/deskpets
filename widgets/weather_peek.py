"""WeatherPeek - Current weather from wttr.in (no API key needed)."""
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
    DOCK_TO_BAR = True  # every hour

    def _build(self):
        self.city = self.config.get("weather_city", "")
        self.temp_label = tk.Label(self.win, text="🌤 --°C", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT_LARGE, anchor="w")
        self.temp_label.pack(fill=tk.X, padx=8, pady=(6, 0))
        self.desc_label = tk.Label(self.win, text="Loading...", bg=self.BG_COLOR, fg="#888", font=self.FONT_SMALL, anchor="w")
        self.desc_label.pack(fill=tk.X, padx=8, pady=(0, 6))

    def _update(self):
        if not requests:
            self.desc_label.config(text="pip install requests")
            return
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            url = f"https://wttr.in/{self.city}?format=j1"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]
            feels = current["FeelsLikeC"]
            self.win.after(0, lambda: self._show(temp, desc, feels))
        except Exception:
            self.win.after(0, lambda: self.desc_label.config(text="Failed to fetch"))

    def _show(self, temp, desc, feels):
        self.temp_label.config(text=f"🌤 {temp}°C (feels {feels}°C)")
        self.desc_label.config(text=desc)
