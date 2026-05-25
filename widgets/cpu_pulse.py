"""CPUPulse - CPU, RAM, Disk usage bars."""
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
        self.cpu_label = tk.Label(self.win, text="CPU: --", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT, anchor="w")
        self.cpu_label.pack(fill=tk.X, padx=8, pady=(6, 0))
        self.cpu_bar = tk.Canvas(self.win, height=8, bg="#333", highlightthickness=0)
        self.cpu_bar.pack(fill=tk.X, padx=8, pady=2)

        self.ram_label = tk.Label(self.win, text="RAM: --", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT, anchor="w")
        self.ram_label.pack(fill=tk.X, padx=8)
        self.ram_bar = tk.Canvas(self.win, height=8, bg="#333", highlightthickness=0)
        self.ram_bar.pack(fill=tk.X, padx=8, pady=2)

        self.disk_label = tk.Label(self.win, text="Disk: --", bg=self.BG_COLOR, fg=self.FG_COLOR, font=self.FONT, anchor="w")
        self.disk_label.pack(fill=tk.X, padx=8)
        self.disk_bar = tk.Canvas(self.win, height=8, bg="#333", highlightthickness=0)
        self.disk_bar.pack(fill=tk.X, padx=8, pady=(2, 6))

    def _update(self):
        if not psutil:
            self.cpu_label.config(text="CPU: psutil not installed")
            return
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent if not hasattr(psutil.disk_usage, "__call__") or True else 0
        try:
            disk = psutil.disk_usage("C:\\" if os.name == "nt" else "/").percent
        except:
            disk = 0

        self.cpu_label.config(text=f"CPU: {cpu:.0f}%")
        self.ram_label.config(text=f"RAM: {ram:.0f}%")
        self.disk_label.config(text=f"Disk: {disk:.0f}%")

        self._draw_bar(self.cpu_bar, cpu, "#4fc3f7")
        self._draw_bar(self.ram_bar, ram, "#81c784")
        self._draw_bar(self.disk_bar, disk, "#ffb74d" if disk < 90 else "#e57373")

    def _draw_bar(self, canvas, pct, color):
        canvas.delete("all")
        w = canvas.winfo_width()
        fill_w = int(w * pct / 100)
        canvas.create_rectangle(0, 0, fill_w, 10, fill=color, outline="")


import os
