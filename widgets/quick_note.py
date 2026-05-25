"""QuickNote - Sticky note that auto-saves."""
import os
import tkinter as tk

from base import BaseWidget, CONFIG_DIR


class QuickNote(BaseWidget):
    NAME = "QuickNote"
    DEFAULT_WIDTH = 220
    DEFAULT_HEIGHT = 180
    UPDATE_INTERVAL = 5000  # auto-save every 5s
    NOTE_FILE = os.path.join(CONFIG_DIR, "quicknote.txt")

    def _build(self):
        header = tk.Label(self.win, text="📝 Note", bg="#2d2d00", fg="#ffeb3b", font=self.FONT, anchor="w")
        header.pack(fill=tk.X, padx=0, pady=0)

        self.text = tk.Text(self.win, bg="#3d3d1a", fg="#fff9c4", font=self.FONT_SMALL,
                            insertbackground="#ffeb3b", borderwidth=0, highlightthickness=0, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Load saved note
        if os.path.exists(self.NOTE_FILE):
            with open(self.NOTE_FILE, "r") as f:
                self.text.insert("1.0", f.read())

    def _update(self):
        # Auto-save
        content = self.text.get("1.0", tk.END).rstrip()
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(self.NOTE_FILE, "w") as f:
            f.write(content)
