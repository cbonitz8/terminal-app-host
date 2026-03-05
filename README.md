# Terminal App Host

A macOS TUI launcher for personal terminal apps, built with [Textual](https://textual.textualize.io/).

Register your terminal-based apps and launch them from a single dashboard — each app opens in a new Terminal.app window.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)

## Features

- Browse registered apps in a clean terminal UI
- Launch any app with a single keypress — opens in a new Terminal.app window
- Add and remove apps on the fly
- Config persists across sessions in a simple TOML file

## Installation

```bash
git clone https://github.com/cbonitz8/terminal-app-host.git
cd terminal-app-host
pip install -e .
```

## Usage

```bash
terminal-app-host
# or
python -m terminal_app_host
```

### Key Bindings

| Key     | Action              |
|---------|---------------------|
| `Enter` | Launch selected app |
| `a`     | Add a new app       |
| `r`     | Remove selected app |
| `q`     | Quit                |

## Configuration

Apps are stored in `~/.config/terminal-app-host/config.toml`:

```toml
[[apps]]
name = "My App"
path = "/path/to/app"
command = "python3 -m my_app"
description = "A short description"
```

## Requirements

- macOS (uses `osascript` to open Terminal.app windows)
- Python 3.11+
