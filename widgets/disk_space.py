"""DiskSpace - Shows free space on all drives."""
import os
import tkinter as tk
try:
    import psutil
except ImportError:
    psutil = None

from base import BaseWidget


class DiskSpace(BaseWidget):
    NAME = "DiskSpace"
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 100
    UPDATE_INTERVAL = 30000  # every 30s

    def _build(self):
        self.container = tk.Frame(self.win, bg=self.BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self._labels = []

    def _update(self):
        for w in self.container.winfo_children():
            w.destroy()

        if not psutil:
            tk.Label(self.container, text="psutil needed", bg=self.BG_COLOR, fg=self.FG_COLOR).pack()
            return

        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
            except (PermissionError, OSError):
                continue

            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            pct = usage.percent
            color = "#e57373" if pct > 90 else "#ffb74d" if pct > 75 else "#81c784"

            frame = tk.Frame(self.container, bg=self.BG_COLOR)
            frame.pack(fill=tk.X, pady=1)

            tk.Label(frame, text=f"{p.mountpoint}", bg=self.BG_COLOR, fg=self.FG_COLOR,
                     font=self.FONT_SMALL, width=4, anchor="w").pack(side=tk.LEFT)
            tk.Label(frame, text=f"{free_gb:.0f}GB free", bg=self.BG_COLOR, fg=color,
                     font=self.FONT_SMALL).pack(side=tk.RIGHT)
