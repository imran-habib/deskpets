"""CPUPulse - CPU, RAM, Disk usage (compact taskbar mode)."""
import os
import tkinter as tk
try:
    import psutil
except ImportError:
    psutil = None

from base import BaseWidget


class CPUPulse(BaseWidget):
    NAME = "CPUPulse"
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 90
    UPDATE_INTERVAL = 2000
    DOCK_TO_BAR = True

    def _build(self):
        f = ("Segoe UI", 8)
        self.cpu_l = tk.Label(self.win, text="CPU --", bg=self.BG_COLOR, fg="#4fc3f7", font=f)
        self.cpu_l.pack(side=tk.LEFT, padx=2)
        self.ram_l = tk.Label(self.win, text="RAM --", bg=self.BG_COLOR, fg="#81c784", font=f)
        self.ram_l.pack(side=tk.LEFT, padx=2)
        self.disk_l = tk.Label(self.win, text="Disk --", bg=self.BG_COLOR, fg="#ffb74d", font=f)
        self.disk_l.pack(side=tk.LEFT, padx=2)

    def _update(self):
        if not psutil:
            return
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        try:
            disk = psutil.disk_usage("C:\\" if os.name == "nt" else "/").percent
        except:
            disk = 0
        self.cpu_l.config(text=f"CPU {cpu:.0f}%")
        self.ram_l.config(text=f"RAM {ram:.0f}%")
        self.disk_l.config(text=f"Disk {disk:.0f}%")
