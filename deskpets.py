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

        self._create_sidebar()
        self._build_ui()
        self._launch_enabled()
        self._setup_tray()

    def _create_sidebar(self):
        """Create a thin overlay that sits on top of the taskbar (left side)."""
        self.sidebar = tk.Toplevel(self.root)
        self.sidebar.overrideredirect(True)
        self.sidebar.attributes("-topmost", True)
        self.sidebar.attributes("-alpha", 0.95)
        self.sidebar.configure(bg="#202020")

        # Detect screen size and taskbar dimensions
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # DPI scaling factor
        try:
            dpi = self.root.winfo_fpixels('1i')
            scale = dpi / 96.0
        except:
            scale = 1.0

        # Taskbar height on Win 11 is ~48px at 100% scale
        taskbar_h = int(48 * scale)
        bar_h = taskbar_h - 4  # slightly smaller to look embedded

        # Position: bottom of screen, offset from left
        # Win 11 Start button + search/widgets area is ~100px at 100% scale
        start_offset = int(100 * scale)
        bar_w = min(int(screen_w * 0.4), 700)
        x_pos = start_offset
        y_pos = screen_h - taskbar_h + 2

        self.sidebar.geometry(f"{bar_w}x{bar_h}+{x_pos}+{y_pos}")

        # Allow clicks to pass through to taskbar when not on our widgets
        if os.name == "nt":
            try:
                import ctypes
                hwnd = int(self.sidebar.wm_frame(), 16)
                # Don't set click-through, just make sure we don't block Start
            except:
                pass

        # Store scale for widgets to use
        self._scale = scale
        self._bar_font_size = max(8, int(9 * scale))

        # Horizontal frame for widgets
        self.bar_frame = tk.Frame(self.sidebar, bg="#202020")
        self.bar_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)

        self.sidebar.withdraw()

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
        if widget_class.DOCK_TO_BAR:
            widget = widget_class(master=self.root, dock_frame=self.bar_frame)
            self.sidebar.deiconify()  # Show sidebar when bar widgets are active
        else:
            widget = widget_class(master=self.root)
        self._active_widgets[name] = widget

    def _stop_widget(self, name):
        if name in self._active_widgets:
            self._active_widgets[name].close()
            del self._active_widgets[name]
        # Hide sidebar if no bar widgets active
        has_bar = any(ALL_WIDGETS[n].DOCK_TO_BAR for n in self._active_widgets)
        if not has_bar:
            self.sidebar.withdraw()

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
