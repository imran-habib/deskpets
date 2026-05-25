"""CountdownWidget - Countdown to events."""
import json
import os
import tkinter as tk
from datetime import datetime

from base import BaseWidget, CONFIG_DIR


class CountdownWidget(BaseWidget):
    NAME = "Countdown"
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 80
    UPDATE_INTERVAL = 60000
    DOCK_TO_BAR = True  # every minute
    EVENTS_FILE = os.path.join(CONFIG_DIR, "countdowns.json")

    def _build(self):
        self._events = self._load_events()

        header = tk.Frame(self.win, bg=self.BG_COLOR)
        header.pack(fill=tk.X, padx=6, pady=(6, 2))
        tk.Label(header, text="⏳ Countdown", bg=self.BG_COLOR, fg=self.ACCENT_COLOR, font=self.FONT).pack(side=tk.LEFT)
        add_btn = tk.Label(header, text="+", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT_LARGE, cursor="hand2")
        add_btn.pack(side=tk.RIGHT)
        add_btn.bind("<Button-1>", self._add_event)

        self.container = tk.Frame(self.win, bg=self.BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

    def _load_events(self):
        try:
            with open(self.EVENTS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [{"name": "New Year", "date": "2027-01-01"}]

    def _save_events(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(self.EVENTS_FILE, "w") as f:
            json.dump(self._events, f)

    def _update(self):
        for w in self.container.winfo_children():
            w.destroy()

        now = datetime.now()
        for event in self._events[:4]:
            try:
                target = datetime.strptime(event["date"], "%Y-%m-%d")
                days = (target - now).days
                color = "#e57373" if days < 3 else "#ffb74d" if days < 7 else self.FG_COLOR
                text = f"{event['name']}: {days}d" if days >= 0 else f"{event['name']}: passed"
                tk.Label(self.container, text=text, bg=self.BG_COLOR, fg=color, font=self.FONT_SMALL, anchor="w").pack(fill=tk.X)
            except (ValueError, KeyError):
                continue

    def _add_event(self, event=None):
        from tkinter import simpledialog
        name = simpledialog.askstring("Add Countdown", "Event name:", parent=self.win)
        if not name:
            return
        date = simpledialog.askstring("Add Countdown", "Date (YYYY-MM-DD):", parent=self.win)
        if not date:
            return
        self._events.append({"name": name, "date": date})
        self._save_events()
        self._update()
