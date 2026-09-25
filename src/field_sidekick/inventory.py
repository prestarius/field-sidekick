"""Concise, read-only machine and development-tool inventory."""

import platform
import shutil

from rich.console import Console
from rich.table import Table

from field_sidekick.doctor import wifi_interfaces


def render_inventory(console: Console) -> None:
    """Render local platform and installed-tool presence without probing tools."""
    tools = ("git", "docker", "tailscale", "syncthing", "uv")
    table = Table(title="field-sidekick inventory")
    table.add_column("Item")
    table.add_column("Value")
    table.add_row("System", f"{platform.system()} {platform.release()}")
    table.add_row("Machine", platform.machine() or "unknown")
    table.add_row("Python", platform.python_version())
    table.add_row("Wi-Fi", ", ".join(wifi_interfaces()) or "none detected")
    available_tools = ", ".join(tool for tool in tools if shutil.which(tool)) or "none"
    table.add_row("Available tools", available_tools)
    console.print(table)
