"""NetMeter - Upload/Download speed (compact taskbar mode)."""
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

        f = ("Segoe UI", 8)
        self.down_l = tk.Label(self.win, text="↓ 0", bg=self.BG_COLOR, fg="#4fc3f7", font=f)
        self.down_l.pack(side=tk.LEFT, padx=1)
        self.up_l = tk.Label(self.win, text="↑ 0", bg=self.BG_COLOR, fg="#81c784", font=f)
        self.up_l.pack(side=tk.LEFT, padx=1)

    def _update(self):
        if not psutil:
            return
        net = psutil.net_io_counters()
        down = net.bytes_recv - self._last_recv
        up = net.bytes_sent - self._last_sent
        self._last_recv = net.bytes_recv
        self._last_sent = net.bytes_sent
        self.down_l.config(text=f"↓{self._fmt(down)}")
        self.up_l.config(text=f"↑{self._fmt(up)}")

    def _fmt(self, b):
        if b > 1024 * 1024:
            return f"{b/1024/1024:.1f}M"
        if b > 1024:
            return f"{b/1024:.0f}K"
        return f"{b}B"
