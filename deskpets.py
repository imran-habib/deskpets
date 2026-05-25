#!/usr/bin/env python3
"""
DeskPets - Lightweight desktop widgets for Windows 11.
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk

from base import load_config, save_config
from widgets import ALL_WIDGETS

ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deskpets.ico")


class DeskPetsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DeskPets - Widget Selector")
        self.root.geometry("350x400")
        self.root.resizable(False, False)

        if os.path.exists(ICON_PATH):
            try:
                self.root.iconbitmap(ICON_PATH)
            except tk.TclError:
                pass

        self.config = load_config()
        self._active_widgets = {}
        self._vars = {}

        self._build_ui()
        self._launch_enabled()
        self._setup_tray()

    def _build_ui(self):
        ttk.Label(self.root, text="🐾 DeskPets", font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))
        ttk.Label(self.root, text="Select widgets to show on desktop:").pack(pady=(0, 10))

        enabled = set(self.config.get("enabled_widgets", []))

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        descriptions = {
            "CPUPulse": "CPU, RAM, Disk usage bars",
            "NetMeter": "Upload/Download speed",
            "ClipWidget": "Clipboard history",
            "QuickNote": "Sticky note (auto-saves)",
            "PomodoroBar": "25/5 min work timer",
            "DiskSpace": "Free space on all drives",
            "Countdown": "Countdown to events",
            "CommandPal": "Quick command bar",
            "WeatherPeek": "Current weather",
        }

        for name in ALL_WIDGETS:
            var = tk.BooleanVar(value=name in enabled)
            self._vars[name] = var
            desc = descriptions.get(name, "")
            cb = ttk.Checkbutton(frame, text=f"{name}  —  {desc}", variable=var,
                                 command=lambda n=name: self._toggle_widget(n))
            cb.pack(fill=tk.X, pady=2, anchor="w")

        # Buttons
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Enable All", command=self._enable_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Disable All", command=self._disable_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Hide to Tray", command=self._hide_to_tray).pack(side=tk.RIGHT, padx=2)

    def _toggle_widget(self, name):
        if self._vars[name].get():
            self._start_widget(name)
        else:
            self._stop_widget(name)
        self._save_enabled()

    def _start_widget(self, name):
        if name in self._active_widgets:
            return
        widget_class = ALL_WIDGETS[name]
        widget = widget_class(master=self.root)
        self._active_widgets[name] = widget

    def _stop_widget(self, name):
        if name in self._active_widgets:
            self._active_widgets[name].close()
            del self._active_widgets[name]

    def _launch_enabled(self):
        for name in self.config.get("enabled_widgets", []):
            if name in ALL_WIDGETS:
                self._vars[name].set(True)
                self._start_widget(name)

    def _save_enabled(self):
        enabled = [name for name, var in self._vars.items() if var.get()]
        self.config["enabled_widgets"] = enabled
        save_config(self.config)

    def _enable_all(self):
        for name, var in self._vars.items():
            var.set(True)
            self._start_widget(name)
        self._save_enabled()

    def _disable_all(self):
        for name, var in self._vars.items():
            var.set(False)
            self._stop_widget(name)
        self._save_enabled()

    def _hide_to_tray(self):
        self.root.withdraw()

    def _setup_tray(self):
        try:
            import pystray
            from PIL import Image as PILImage

            if os.path.exists(ICON_PATH):
                icon_img = PILImage.open(ICON_PATH)
            else:
                icon_img = PILImage.new("RGB", (64, 64), "purple")

            menu = pystray.Menu(
                pystray.MenuItem("Show Settings", self._show_settings, default=True),
                pystray.MenuItem("Exit", self._exit_app),
            )
            self._tray = pystray.Icon("DeskPets", icon_img, "DeskPets", menu)
            threading.Thread(target=self._tray.run, daemon=True).start()
        except ImportError:
            pass

    def _show_settings(self, *args):
        self.root.after(0, self.root.deiconify)

    def _exit_app(self, *args):
        for name in list(self._active_widgets):
            self._stop_widget(name)
        try:
            self._tray.stop()
        except:
            pass
        self.root.after(0, self.root.destroy)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._hide_to_tray)
        self.root.mainloop()


if __name__ == "__main__":
    app = DeskPetsApp()
    app.run()
