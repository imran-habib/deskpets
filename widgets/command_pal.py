"""CommandPal - Quick command bar."""
import os
import subprocess
import tkinter as tk

from base import BaseWidget


COMMANDS = {
    "ip": lambda: subprocess.check_output("ipconfig" if os.name == "nt" else "ip addr", shell=True).decode()[:200],
    "time": lambda: __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "uptime": lambda: _get_uptime(),
    "empty trash": lambda: _empty_trash(),
    "calc": lambda: subprocess.Popen("calc" if os.name == "nt" else "gnome-calculator", shell=True) or "Opened",
    "notepad": lambda: subprocess.Popen("notepad" if os.name == "nt" else "gedit", shell=True) or "Opened",
}


def _get_uptime():
    try:
        import psutil
        boot = __import__("datetime").datetime.fromtimestamp(psutil.boot_time())
        delta = __import__("datetime").datetime.now() - boot
        hours = int(delta.total_seconds() // 3600)
        mins = int((delta.total_seconds() % 3600) // 60)
        return f"Up {hours}h {mins}m"
    except ImportError:
        return "psutil needed"


def _empty_trash():
    if os.name == "nt":
        import ctypes
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        return "Trash emptied"
    return "Linux: rm -rf ~/.local/share/Trash/*"


class CommandPal(BaseWidget):
    NAME = "CommandPal"
    DEFAULT_WIDTH = 280
    DEFAULT_HEIGHT = 70
    UPDATE_INTERVAL = 60000

    def _build(self):
        frame = tk.Frame(self.win, bg=self.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tk.Label(frame, text="⚡", bg=self.BG_COLOR, fg=self.ACCENT_COLOR, font=self.FONT).pack(side=tk.LEFT)

        self.entry = tk.Entry(frame, bg="#2a2a2a", fg=self.FG_COLOR, font=self.FONT,
                              insertbackground=self.FG_COLOR, borderwidth=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        self.entry.bind("<Return>", self._run_command)

        self.result_label = tk.Label(self.win, text="Type a command...", bg=self.BG_COLOR,
                                     fg="#888", font=self.FONT_SMALL, anchor="w")
        self.result_label.pack(fill=tk.X, padx=8, pady=(0, 4))

    def _run_command(self, event=None):
        cmd = self.entry.get().strip().lower()
        if cmd in COMMANDS:
            try:
                result = COMMANDS[cmd]()
                self.result_label.config(text=str(result)[:80], fg=self.ACCENT_COLOR)
            except Exception as e:
                self.result_label.config(text=str(e)[:80], fg="#e57373")
        else:
            # Try running as shell command
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode().strip()
                self.result_label.config(text=result[:80], fg=self.FG_COLOR)
            except Exception as e:
                self.result_label.config(text=f"Unknown: {cmd}", fg="#e57373")
        self.entry.delete(0, tk.END)

    def _update(self):
        pass
