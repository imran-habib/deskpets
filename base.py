"""
DeskPets - Base widget framework.
Floating borderless windows that stay on desktop, draggable, remember position.
"""
import json
import os
import tkinter as tk
from typing import Optional

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".deskpets")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> dict:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"enabled_widgets": [], "positions": {}, "opacity": {}}


def save_config(config: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


class BaseWidget:
    """Base class for all DeskPets widgets."""

    NAME = "Widget"
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 80
    UPDATE_INTERVAL = 1000  # ms
    BG_COLOR = "#1e1e1e"
    FG_COLOR = "#e0e0e0"
    ACCENT_COLOR = "#4fc3f7"
    FONT = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_LARGE = ("Segoe UI", 12, "bold")
    DOCK_TO_BAR = False  # If True, widget docks to left sidebar instead of floating

    def __init__(self, master: Optional[tk.Tk] = None, dock_frame: Optional[tk.Frame] = None):
        self.dock_frame = dock_frame

        if dock_frame and self.DOCK_TO_BAR:
            # Docked mode: embed in taskbar overlay (horizontal)
            self.win = tk.Frame(dock_frame, bg=self.BG_COLOR)
            self.win.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
            # Add separator
            sep = tk.Frame(dock_frame, bg="#444", width=1)
            sep.pack(side=tk.LEFT, fill=tk.Y, padx=2)
            self._build()
            self._start_updates()
        else:
            # Floating mode
            if master:
                self.win = tk.Toplevel(master)
            else:
                self.win = tk.Tk()
            self.config = load_config()
            self._drag_data = {"x": 0, "y": 0}
            self._setup_window()
            self._build()
            self._enable_drag()
            self._start_updates()

    def _setup_window(self):
        self.win.overrideredirect(True)  # No title bar/border
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", self.config.get("opacity", {}).get(self.NAME, 0.92))
        self.win.configure(bg=self.BG_COLOR)

        # Restore position or center
        pos = self.config.get("positions", {}).get(self.NAME)
        if pos:
            self.win.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}+{pos[0]}+{pos[1]}")
        else:
            self.win.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}+100+100")

        # Right-click to close
        self.win.bind("<Button-3>", self._show_menu)

        # Context menu
        self.menu = tk.Menu(self.win, tearoff=0)
        self.menu.add_command(label=f"Close {self.NAME}", command=self.close)

    def _enable_drag(self):
        self.win.bind("<Button-1>", self._drag_start)
        self.win.bind("<B1-Motion>", self._drag_move)
        self.win.bind("<ButtonRelease-1>", self._drag_stop)

    def _drag_start(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _drag_move(self, event):
        x = self.win.winfo_x() + event.x - self._drag_data["x"]
        y = self.win.winfo_y() + event.y - self._drag_data["y"]
        self.win.geometry(f"+{x}+{y}")

    def _drag_stop(self, event):
        # Save position
        x = self.win.winfo_x()
        y = self.win.winfo_y()
        self.config = load_config()
        if "positions" not in self.config:
            self.config["positions"] = {}
        self.config["positions"][self.NAME] = [x, y]
        save_config(self.config)

    def _show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def _build(self):
        """Override: build widget UI."""
        pass

    def _update(self):
        """Override: update widget data."""
        pass

    def _start_updates(self):
        self._update()
        self.win.after(self.UPDATE_INTERVAL, self._start_updates)

    def close(self):
        if self.dock_frame and self.DOCK_TO_BAR:
            self.win.destroy()
        else:
            self.win.destroy()
