# CLAUDE.md

## Project: Terminal App Host

A macOS TUI launcher for personal terminal apps, built with [Textual](https://textual.textualize.io/). Lets you register, browse, and launch terminal-based apps from a single dashboard. Launching opens a new macOS Terminal.app window via `osascript`.

## Architecture

```
src/terminal_app_host/
├── __main__.py   # Entry point — instantiates and runs the Textual app
├── app.py        # Main TUI (TerminalAppHost), app list UI, and AddAppScreen modal
├── app.tcss      # Textual CSS styles
└── config.py     # TOML config loading/saving, AppEntry dataclass
```

- **app.py** — `TerminalAppHost` (main App): shows ASCII logo, a `ListView` of registered apps, and a footer with keybindings. `AddAppScreen` is a modal for registering new apps. Launching uses `osascript` to open a Terminal.app window that `cd`s and runs the command.
- **config.py** — Config lives at `~/.config/terminal-app-host/config.toml`. Each app entry has `name`, `path`, `command`, and optional `description`. Provides `load_config`, `save_config`, `add_app`, `remove_app`.

## Key Bindings

| Key     | Action     |
|---------|------------|
| `Enter` | Launch app |
| `a`     | Add app    |
| `r`     | Remove app |
| `q`     | Quit       |

## Tech Stack

- Python 3.11+
- Textual (TUI framework)
- Hatchling (build system)
- TOML config (`tomllib` stdlib)
- macOS-only (uses `osascript` for Terminal.app integration)

## Running

```sh
# Install in dev mode
pip install -e .

# Run
terminal-app-host
# or
python -m terminal_app_host
```

## Guidelines

- Use clear, concise code with minimal abstractions
- Prefer simple solutions over clever ones
- Keep files focused and single-purpose
- Write code that is easy to read and maintain

## Workflow Preferences

- Run commands freely without confirmation for local dev tasks (build, test, lint, install)
- Edit and create files as needed
- Use git freely for local operations (commit, branch, stash, etc.)
- Read any files in the project without restriction
