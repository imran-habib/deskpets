"""PomodoroBar - Tiny pomodoro timer."""
import tkinter as tk

from base import BaseWidget


class PomodoroBar(BaseWidget):
    NAME = "PomodoroBar"
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 50
    UPDATE_INTERVAL = 1000

    def _build(self):
        self._running = False
        self._seconds_left = 25 * 60
        self._is_break = False

        frame = tk.Frame(self.win, bg=self.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.time_label = tk.Label(frame, text="25:00", bg=self.BG_COLOR, fg="#e57373", font=("Segoe UI", 14, "bold"))
        self.time_label.pack(side=tk.LEFT, padx=(0, 8))

        self.status_label = tk.Label(frame, text="WORK", bg=self.BG_COLOR, fg="#e57373", font=self.FONT_SMALL)
        self.status_label.pack(side=tk.LEFT)

        self.btn = tk.Label(frame, text="▶", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT_LARGE, cursor="hand2")
        self.btn.pack(side=tk.RIGHT)
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
                self.status_label.config(text="BREAK" if self._is_break else "WORK", fg=color)
                self.time_label.config(fg=color)

        mins, secs = divmod(self._seconds_left, 60)
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
