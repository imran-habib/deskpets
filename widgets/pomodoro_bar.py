"""PomodoroBar - Tiny pomodoro timer (compact taskbar mode)."""
import tkinter as tk

from base import BaseWidget


class PomodoroBar(BaseWidget):
    NAME = "PomodoroBar"
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 50
    UPDATE_INTERVAL = 1000
    DOCK_TO_BAR = True

    def _build(self):
        self._running = False
        self._seconds_left = 25 * 60
        self._is_break = False

        f = ("Segoe UI", 8)
        self.time_l = tk.Label(self.win, text="⏱25:00", bg=self.BG_COLOR, fg="#e57373", font=("Segoe UI", 9, "bold"))
        self.time_l.pack(side=tk.LEFT, padx=2)

        self.btn = tk.Label(self.win, text="▶", bg=self.BG_COLOR, fg=self.FG_COLOR, font=f, cursor="hand2")
        self.btn.pack(side=tk.LEFT, padx=1)
        self.btn.bind("<Button-1>", self._toggle)

    def _toggle(self, event=None):
        self._running = not self._running
        self.btn.config(text="⏸" if self._running else "▶")

    def _update(self):
        if self._running:
            self._seconds_left -= 1
            if self._seconds_left <= 0:
                self._is_break = not self._is_break
                self._seconds_left = 5 * 60 if self._is_break else 25 * 60
                color = "#81c784" if self._is_break else "#e57373"
                self.time_l.config(fg=color)

        mins, secs = divmod(self._seconds_left, 60)
        prefix = "☕" if self._is_break else "⏱"
        self.time_l.config(text=f"{prefix}{mins:02d}:{secs:02d}")
