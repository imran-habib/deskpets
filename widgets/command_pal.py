"""CommandPal - Quick command bar with expandable output and history."""
import os
import subprocess
import tkinter as tk

from base import BaseWidget


COMMANDS = {
    "ip": "ipconfig" if os.name == "nt" else "ip addr",
    "time": "echo %date% %time%" if os.name == "nt" else "date",
    "uptime": "net stats workstation | find \"since\"" if os.name == "nt" else "uptime",
    "wifi": "netsh wlan show interfaces | find \"SSID\"" if os.name == "nt" else "iwgetid -r",
    "battery": "WMIC PATH Win32_Battery Get EstimatedChargeRemaining" if os.name == "nt" else "cat /sys/class/power_supply/BAT0/capacity",
    "ports": "netstat -an | find \"LISTENING\"" if os.name == "nt" else "ss -tlnp",
    "flush dns": "ipconfig /flushdns" if os.name == "nt" else "sudo systemd-resolve --flush-caches",
    "lock": "rundll32.exe user32.dll,LockWorkStation" if os.name == "nt" else "xdg-screensaver lock",
    "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0" if os.name == "nt" else "systemctl suspend",
    "open downloads": "explorer Downloads" if os.name == "nt" else "xdg-open ~/Downloads",
    "calc": "calc" if os.name == "nt" else "gnome-calculator",
    "notepad": "notepad" if os.name == "nt" else "gedit",
}


class CommandPal(BaseWidget):
    NAME = "CommandPal"
    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 250
    UPDATE_INTERVAL = 60000

    def _build(self):
        self._history = []
        self._history_idx = -1

        # Input frame
        input_frame = tk.Frame(self.win, bg=self.BG_COLOR)
        input_frame.pack(fill=tk.X, padx=6, pady=(6, 2))

        tk.Label(input_frame, text="⚡", bg=self.BG_COLOR, fg=self.ACCENT_COLOR, font=self.FONT).pack(side=tk.LEFT)

        self.entry = tk.Entry(input_frame, bg="#2a2a2a", fg=self.FG_COLOR, font=("Consolas", 10),
                              insertbackground=self.FG_COLOR, borderwidth=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        self.entry.bind("<Return>", self._run_command)
        self.entry.bind("<Up>", self._history_up)
        self.entry.bind("<Down>", self._history_down)

        # Output area (scrollable, expandable)
        self.output = tk.Text(self.win, bg="#1a1a1a", fg=self.FG_COLOR, font=("Consolas", 9),
                              borderwidth=0, highlightthickness=0, wrap=tk.WORD, state=tk.DISABLED)
        self.output.pack(fill=tk.BOTH, expand=True, padx=6, pady=(2, 6))

        # Make window resizable
        self.win.overrideredirect(False)
        self.win.overrideredirect(True)
        # Add resize grip
        grip = tk.Label(self.win, text="⋮⋮", bg=self.BG_COLOR, fg="#555", cursor="sizing")
        grip.place(relx=1.0, rely=1.0, anchor="se")
        grip.bind("<B1-Motion>", self._resize)

        self._append_output("DeskPets CommandPal\nType a command or 'help' for built-in commands.\n")

    def _run_command(self, event=None):
        cmd = self.entry.get().strip()
        if not cmd:
            return
        self.entry.delete(0, tk.END)

        # Add to history
        if not self._history or self._history[-1] != cmd:
            self._history.append(cmd)
        self._history_idx = len(self._history)

        self._append_output(f"\n> {cmd}\n")

        if cmd.lower() == "help":
            self._show_help()
            return
        if cmd.lower() == "clear":
            self.output.config(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            self.output.config(state=tk.DISABLED)
            return

        # Resolve built-in aliases
        shell_cmd = COMMANDS.get(cmd.lower(), cmd)

        # Handle "kill <process>" shortcut
        if cmd.lower().startswith("kill "):
            proc = cmd[5:].strip()
            shell_cmd = f"taskkill /f /im {proc}.exe" if os.name == "nt" else f"pkill -f {proc}"

        # Run command
        try:
            result = subprocess.run(
                shell_cmd, shell=True, capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if result.stderr.strip():
                output += ("\n" if output else "") + result.stderr.strip()
            if not output:
                output = "(no output)"
            self._append_output(output + "\n")
        except subprocess.TimeoutExpired:
            self._append_output("Error: Command timed out (10s limit)\n")
        except Exception as e:
            self._append_output(f"Error: {e}\n")

    def _show_help(self):
        help_text = "Built-in commands:\n"
        for cmd in sorted(COMMANDS.keys()):
            help_text += f"  {cmd}\n"
        help_text += "  kill <name>  — kill a process\n"
        help_text += "  clear        — clear output\n"
        help_text += "  help         — show this\n"
        help_text += "\nAnything else runs as a shell command.\n"
        self._append_output(help_text)

    def _append_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def _history_up(self, event=None):
        if self._history and self._history_idx > 0:
            self._history_idx -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self._history[self._history_idx])

    def _history_down(self, event=None):
        if self._history_idx < len(self._history) - 1:
            self._history_idx += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self._history[self._history_idx])
        else:
            self._history_idx = len(self._history)
            self.entry.delete(0, tk.END)

    def _resize(self, event):
        x = self.win.winfo_pointerx() - self.win.winfo_rootx()
        y = self.win.winfo_pointery() - self.win.winfo_rooty()
        self.win.geometry(f"{max(x, 250)}x{max(y, 100)}")

    def _update(self):
        pass
