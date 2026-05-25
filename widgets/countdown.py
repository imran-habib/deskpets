"""CountdownWidget - Countdown to events (compact taskbar mode)."""
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
    DOCK_TO_BAR = True
    EVENTS_FILE = os.path.join(CONFIG_DIR, "countdowns.json")

    def _build(self):
        self._events = self._load_events()
        self._label = tk.Label(self.win, text="", bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Segoe UI", 8))
        self._label.pack(side=tk.LEFT, padx=2)
        self._label.bind("<Button-1>", self._add_event)

    def _load_events(self):
        try:
            with open(self.EVENTS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [{"name": "NY", "date": "2027-01-01"}]

    def _save_events(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(self.EVENTS_FILE, "w") as f:
            json.dump(self._events, f)

    def _update(self):
        now = datetime.now()
        parts = []
        for event in self._events[:3]:
            try:
                target = datetime.strptime(event["date"], "%Y-%m-%d")
                days = (target - now).days
                if days >= 0:
                    parts.append(f"{event['name']}:{days}d")
            except (ValueError, KeyError):
                continue
        self._label.config(text=" | ".join(parts) if parts else "⏳ click to add")

    def _add_event(self, event=None):
        from tkinter import simpledialog
        name = simpledialog.askstring("Countdown", "Event name:", parent=self.win)
        if not name:
            return
        date = simpledialog.askstring("Countdown", "Date (YYYY-MM-DD):", parent=self.win)
        if not date:
            return
        self._events.append({"name": name, "date": date})
        self._save_events()
        self._update()
