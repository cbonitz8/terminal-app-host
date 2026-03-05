from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "terminal-app-host"
CONFIG_PATH = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = """\
[[apps]]
name = "Video Caster"
path = "/Users/caleb/git stuff/video-caster"
command = "python3 -m video_caster"
description = "Cast local videos to Chromecast, Apple TV, and DLNA devices"
"""


@dataclass
class AppEntry:
    name: str
    path: str
    command: str
    description: str = ""


def load_config() -> list[AppEntry]:
    if not CONFIG_PATH.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(DEFAULT_CONFIG)

    data = tomllib.loads(CONFIG_PATH.read_text())
    return [AppEntry(**app) for app in data.get("apps", [])]


def save_config(apps: list[AppEntry]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for app in apps:
        lines.append("[[apps]]")
        lines.append(f'name = "{app.name}"')
        lines.append(f'path = "{app.path}"')
        lines.append(f'command = "{app.command}"')
        if app.description:
            lines.append(f'description = "{app.description}"')
        lines.append("")
    CONFIG_PATH.write_text("\n".join(lines))


def add_app(app: AppEntry) -> list[AppEntry]:
    apps = load_config()
    apps.append(app)
    save_config(apps)
    return apps


def remove_app(name: str) -> list[AppEntry]:
    apps = [a for a in load_config() if a.name != name]
    save_config(apps)
    return apps
