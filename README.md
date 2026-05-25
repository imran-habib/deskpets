# DeskPets 🐾

Lightweight desktop widgets for Windows 11. Pick the ones you want — they float on your desktop, always visible, using minimal resources.

## Widgets

| Widget | What it does |
|--------|-------------|
| **CPUPulse** | CPU, RAM, Disk usage bars |
| **NetMeter** | Live upload/download speed |
| **ClipWidget** | Clipboard history (last 15 clips) |
| **QuickNote** | Sticky note that auto-saves |
| **PomodoroBar** | 25/5 min work/break timer |
| **DiskSpace** | Free space on all drives |
| **Countdown** | Countdown to events/deadlines |
| **CommandPal** | Quick command bar (type "ip", "time", "calc", etc.) |
| **WeatherPeek** | Current weather (no API key needed) |

## Installation

### Windows
Download `DeskPets.exe` from [Releases](https://github.com/imran-habib/deskpets/releases) — double-click to run.

### From Source
```bash
git clone https://github.com/imran-habib/deskpets.git
cd deskpets
pip install psutil requests
python deskpets.py
```

## How it works

1. Double-click `DeskPets.exe` → Settings window opens
2. Check the widgets you want → they appear on your desktop
3. Drag widgets anywhere — they remember their position
4. Close the settings window → app minimizes to system tray
5. Widgets stay on desktop, always visible

## Features

- **Selectable** — enable/disable any widget from the settings panel
- **Draggable** — drag widgets anywhere on your desktop
- **Remembers position** — widgets stay where you put them
- **Always on top** — visible over other windows
- **System tray** — runs silently in background
- **Low resources** — ~15-25 MB RAM total for all widgets
- **Right-click** — right-click any widget to close it
- **Auto-save** — QuickNote saves automatically, Countdown persists events

## Customizing

**To change a widget's appearance:**
Edit the widget file in `widgets/` — each has style constants at the top:
```python
BG_COLOR = "#1e1e1e"    # Background
FG_COLOR = "#e0e0e0"    # Text color
ACCENT_COLOR = "#4fc3f7" # Highlight color
```

**To add a new widget:**
1. Create `widgets/my_widget.py` extending `BaseWidget`
2. Add it to `widgets/__init__.py`
3. It appears in the settings panel automatically

## CommandPal built-in commands

| Command | Action |
|---------|--------|
| `ip` | Show IP address |
| `time` | Show current time |
| `uptime` | Show system uptime |
| `calc` | Open calculator |
| `notepad` | Open notepad |
| `empty trash` | Empty recycle bin |
| Any other | Runs as shell command |

## Project structure

```
deskpets/
├── deskpets.py         # Main app + settings GUI
├── base.py             # Base widget framework
├── deskpets.ico        # App icon
├── widgets/
│   ├── __init__.py     # Widget registry
│   ├── cpu_pulse.py    # CPU/RAM/Disk
│   ├── net_meter.py    # Network speed
│   ├── clip_widget.py  # Clipboard history
│   ├── quick_note.py   # Sticky note
│   ├── pomodoro_bar.py # Pomodoro timer
│   ├── disk_space.py   # Drive space
│   ├── countdown.py    # Event countdown
│   ├── command_pal.py  # Command bar
│   └── weather_peek.py # Weather
└── .github/workflows/  # Auto-build
```

## License

MIT
