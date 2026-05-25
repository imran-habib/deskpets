"""ClipWidget - Clipboard history, click to paste."""
import tkinter as tk

from base import BaseWidget


class ClipWidget(BaseWidget):
    NAME = "ClipWidget"
    DEFAULT_WIDTH = 220
    DEFAULT_HEIGHT = 200
    UPDATE_INTERVAL = 500

    def _build(self):
        self._history = []
        self._last_clip = ""

        header = tk.Label(self.win, text="📋 Clipboard", bg=self.BG_COLOR, fg=self.ACCENT_COLOR, font=self.FONT, anchor="w")
        header.pack(fill=tk.X, padx=8, pady=(6, 2))

        self.listbox = tk.Listbox(self.win, bg="#2a2a2a", fg=self.FG_COLOR, font=self.FONT_SMALL,
                                  selectbackground=self.ACCENT_COLOR, borderwidth=0, highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
        self.listbox.bind("<Double-1>", self._paste_selected)

    def _update(self):
        try:
            clip = self.win.clipboard_get()
        except tk.TclError:
            return

        if clip and clip != self._last_clip:
            self._last_clip = clip
            # Add to history (max 15)
            display = clip.strip().replace("\n", " ")[:50]
            if display and display not in self._history:
                self._history.insert(0, display)
                self._history = self._history[:15]
                self.listbox.delete(0, tk.END)
                for item in self._history:
                    self.listbox.insert(tk.END, item)

    def _paste_selected(self, event):
        sel = self.listbox.curselection()
        if sel:
            text = self._history[sel[0]]
            self.win.clipboard_clear()
            self.win.clipboard_append(text)
