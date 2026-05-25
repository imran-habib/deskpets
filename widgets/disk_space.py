"""DiskSpace - Free space on drives (compact taskbar mode)."""
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
    UPDATE_INTERVAL = 30000
    DOCK_TO_BAR = True

    def _build(self):
        self._labels = []

    def _update(self):
        for w in self.win.winfo_children():
            w.destroy()

        if not psutil:
            return

        f = ("Segoe UI", 8)
        for p in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(p.mountpoint)
            except (PermissionError, OSError):
                continue
            free_gb = usage.free / (1024**3)
            pct = usage.percent
            color = "#e57373" if pct > 90 else "#ffb74d" if pct > 75 else "#81c784"
            drive = p.mountpoint.rstrip("\\/")
            tk.Label(self.win, text=f"{drive}:{free_gb:.0f}G", bg=self.BG_COLOR, fg=color, font=f).pack(side=tk.LEFT, padx=1)
