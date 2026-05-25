# DeskPets 🐾

Lightweight desktop widgets for Windows 11. Pick the ones you want — compact widgets dock to your taskbar, while interactive ones float on your desktop. Minimal resources.

## Widgets

| Widget | What it does | Mode |
|--------|-------------|------|
| **CPUPulse** | CPU, RAM, Disk usage | Taskbar |
| **NetMeter** | Live upload/download speed | Taskbar |
| **PomodoroBar** | 25/5 min work/break timer | Taskbar |
| **DiskSpace** | Free space on all drives | Taskbar |
| **Countdown** | Countdown to events/deadlines | Taskbar |
| **WeatherPeek** | Current weather (no API key needed) | Taskbar |
| **ClipWidget** | Clipboard history (last 15 clips) | Floating |
| **QuickNote** | Sticky note that auto-saves | Floating |
| **CommandPal** | Command bar with history, resizable output | Floating |

## Installation

### Windows
Download `DeskPets.exe` from [Releases](https://github.com/imran-habib/deskpets/releases) — double-click to run.

### From Source
```bash
git clone https://github.com/imran-habib/deskpets.git
cd deskpets
pip install psutil requests pystray Pillow
python deskpets.py
```

## How it works

1. Double-click `DeskPets.exe` → Settings window opens
2. Check the widgets you want → they appear
3. **Taskbar widgets** dock to a thin overlay on the left side of your taskbar
4. **Floating widgets** appear as draggable windows on your desktop
5. Close the settings window → app minimizes to system tray
6. Widgets stay active in the background

## Features

- **Taskbar overlay** — compact widgets sit on top of the taskbar (left side), auto-scales with DPI
- **Floating widgets** — draggable, remember position between sessions
- **Selectable** — enable/disable any widget from the settings panel
- **Always on top** — visible over other windows
- **System tray** — runs silently in background
- **Single instance** — second launch brings existing window to front instead of opening duplicate
- **Low resources** — ~15-25 MB RAM total
- **DPI aware** — auto-adjusts for different screen sizes and resolutions
- **Right-click** — right-click any floating widget to close it

## CommandPal

A mini terminal with built-in commands and full shell access:

| Command | Action |
|---------|--------|
| `ip` | Show IP address |
| `time` | Current date/time |
| `uptime` | System uptime |
| `wifi` | WiFi network name |
| `battery` | Battery percentage |
| `ports` | Listening ports |
| `flush dns` | Flush DNS cache |
| `lock` | Lock screen |
| `sleep` | Sleep PC |
| `open downloads` | Open Downloads folder |
| `calc` | Open calculator |
| `notepad` | Open notepad |
| `kill <name>` | Kill process (e.g., `kill chrome`) |
| `clear` | Clear output |
| `help` | Show all commands |
| Anything else | Runs as shell command (full output) |

- **Up/Down arrows** — cycle through command history
- **Resizable** — drag bottom-right corner to expand output area

## Customizing

**To change a widget's appearance:**
Edit the widget file in `widgets/` — each has style constants:
```python
BG_COLOR = "#1e1e1e"
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
```

**To add a new widget:**
1. Create `widgets/my_widget.py` extending `BaseWidget`
2. Set `DOCK_TO_BAR = True` for taskbar widgets, or `False` for floating
3. Add it to `widgets/__init__.py`
4. It appears in the settings panel automatically

## Project structure

```
deskpets/
├── deskpets.py         # Main app + settings GUI + taskbar overlay
├── base.py             # Base widget framework (floating + docked modes)
├── single_instance.py  # Prevent duplicate instances
├── deskpets.ico        # App icon
├── widgets/
│   ├── __init__.py     # Widget registry
│   ├── cpu_pulse.py    # CPU/RAM/Disk (taskbar)
│   ├── net_meter.py    # Network speed (taskbar)
│   ├── pomodoro_bar.py # Pomodoro timer (taskbar)
│   ├── disk_space.py   # Drive space (taskbar)
│   ├── countdown.py    # Event countdown (taskbar)
│   ├── weather_peek.py # Weather (taskbar)
│   ├── clip_widget.py  # Clipboard history (floating)
│   ├── quick_note.py   # Sticky note (floating)
│   └── command_pal.py  # Command bar (floating)
└── .github/workflows/  # Auto-build
```

## License

MIT
