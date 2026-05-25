"""NetMeter - Upload/Download speed meter."""
import tkinter as tk
try:
    import psutil
except ImportError:
    psutil = None

from base import BaseWidget


class NetMeter(BaseWidget):
    NAME = "NetMeter"
    DEFAULT_WIDTH = 160
    DEFAULT_HEIGHT = 60
    UPDATE_INTERVAL = 1000
    DOCK_TO_BAR = True

    def _build(self):
        self._last_recv = 0
        self._last_sent = 0
        if psutil:
            net = psutil.net_io_counters()
            self._last_recv = net.bytes_recv
            self._last_sent = net.bytes_sent

        self.down_label = tk.Label(self.win, text="↓ 0 KB/s", bg=self.BG_COLOR, fg="#4fc3f7", font=self.FONT_LARGE, anchor="w")
        self.down_label.pack(fill=tk.X, padx=8, pady=(6, 0))

        self.up_label = tk.Label(self.win, text="↑ 0 KB/s", bg=self.BG_COLOR, fg="#81c784", font=self.FONT, anchor="w")
        self.up_label.pack(fill=tk.X, padx=8, pady=(0, 6))

    def _update(self):
        if not psutil:
            return
        net = psutil.net_io_counters()
        down = net.bytes_recv - self._last_recv
        up = net.bytes_sent - self._last_sent
        self._last_recv = net.bytes_recv
        self._last_sent = net.bytes_sent

        self.down_label.config(text=f"↓ {self._fmt(down)}/s")
        self.up_label.config(text=f"↑ {self._fmt(up)}/s")

    def _fmt(self, b):
        if b > 1024 * 1024:
            return f"{b / 1024 / 1024:.1f} MB"
        if b > 1024:
            return f"{b / 1024:.0f} KB"
        return f"{b} B"
