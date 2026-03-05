from __future__ import annotations

import subprocess

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, Center
from textual.screen import ModalScreen
from textual.widgets import Footer, Static, ListItem, ListView, Input, Button, Label

from .config import AppEntry, load_config, add_app, remove_app

LOGO = r"""
 _____ ______________  ________ _   _   ___   _
|_   _|  ___| ___ \  \/  |_   _| \ | | / _ \ | |
  | | | |__ | |_/ / .  . | | | |  \| |/ /_\ \| |        O
  | | |  __||    /| |\/| | | | | . ` ||  _  || |       /|\---+
  | | | |___| |\ \| |  | |_| |_| |\  || | | || |____   / \   |
  \_/ \____/\_| \_\_|  |_/\___/\_| \_/\_| |_/\_____/          +

          _   _ _____ _____ _____                             O
         | | | |  _  /  ___|_   _|                           /|\
         | |_| | | | \ `--.  | |                             / \
         |  _  | | | |`--. \ | |
         | | | \ \_/ /\__/ / | |
         \_| |_/\___/\____/  \_/
"""

TAGLINE = "━━━ your apps, one keypress away ━━━"


class AppItem(ListItem):
    def __init__(self, app_entry: AppEntry) -> None:
        super().__init__()
        self.app_entry = app_entry

    def compose(self) -> ComposeResult:
        yield Static(f"  ▸ {self.app_entry.name}", classes="app-name")
        if self.app_entry.description:
            yield Static(f"    {self.app_entry.description}", classes="app-desc")


class AddAppScreen(ModalScreen[AppEntry | None]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="add-dialog"):
            yield Static("╔══════════════════════════════════════╗", id="dialog-border-top")
            yield Static("║         ✦  R E G I S T E R  ✦       ║", id="dialog-title")
            yield Static("╚══════════════════════════════════════╝", id="dialog-border-bot")
            yield Input(placeholder="Name", id="input-name")
            yield Input(placeholder="Path (working directory)", id="input-path")
            yield Input(placeholder="Command to run", id="input-command")
            yield Input(placeholder="Description (optional)", id="input-desc")
            with Horizontal(id="add-buttons"):
                yield Button("[ Add ]", variant="primary", id="btn-add")
                yield Button("[ Cancel ]", id="btn-cancel")

    @on(Button.Pressed, "#btn-add")
    def on_add(self) -> None:
        name = self.query_one("#input-name", Input).value.strip()
        path = self.query_one("#input-path", Input).value.strip()
        command = self.query_one("#input-command", Input).value.strip()
        desc = self.query_one("#input-desc", Input).value.strip()
        if name and path and command:
            self.dismiss(AppEntry(name=name, path=path, command=command, description=desc))

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self) -> None:
        self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class TerminalAppHost(App):
    CSS_PATH = "app.tcss"
    TITLE = "Terminal Host"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("enter", "launch", "Launch"),
        Binding("a", "add_app", "Add App"),
        Binding("r", "remove_app", "Remove App"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.apps: list[AppEntry] = []

    def compose(self) -> ComposeResult:
        with Center(id="logo-container"):
            yield Static(LOGO, id="logo")
        with Center():
            yield Static(TAGLINE, id="tagline")
        with Vertical(id="app-list-container") as container:
            container.border_title = "Apps"
            yield ListView(id="app-list")
        yield Footer()

    def on_mount(self) -> None:
        self.reload_apps()

    def reload_apps(self) -> None:
        self.apps = load_config()
        list_view = self.query_one("#app-list", ListView)
        list_view.clear()
        if not self.apps:
            list_view.append(ListItem(Static("    (no apps registered — press 'a' to add one)")))
        else:
            for app_entry in self.apps:
                list_view.append(AppItem(app_entry))

    def get_selected_app(self) -> AppEntry | None:
        list_view = self.query_one("#app-list", ListView)
        if list_view.highlighted_child is not None and isinstance(list_view.highlighted_child, AppItem):
            return list_view.highlighted_child.app_entry
        return None

    def action_launch(self) -> None:
        app_entry = self.get_selected_app()
        if app_entry is None:
            self.notify("No app selected", severity="warning")
            return
        self.launch_in_terminal(app_entry)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, AppItem):
            self.launch_in_terminal(event.item.app_entry)

    def launch_in_terminal(self, app_entry: AppEntry) -> None:
        script = f'tell application "Terminal" to do script "cd \'{app_entry.path}\' && {app_entry.command}"'
        subprocess.run(["osascript", "-e", script])
        self.notify(f"Launched {app_entry.name}")

    def action_add_app(self) -> None:
        def on_dismiss(result: AppEntry | None) -> None:
            if result is not None:
                add_app(result)
                self.reload_apps()
                self.notify(f"Added {result.name}")

        self.push_screen(AddAppScreen(), callback=on_dismiss)

    def action_remove_app(self) -> None:
        app_entry = self.get_selected_app()
        if app_entry is None:
            self.notify("No app selected", severity="warning")
            return
        remove_app(app_entry.name)
        self.reload_apps()
        self.notify(f"Removed {app_entry.name}")
