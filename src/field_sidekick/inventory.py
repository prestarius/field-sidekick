"""Concise, read-only machine and development-tool inventory."""

from rich.console import Console
from rich.table import Table

from field_sidekick.core import SidekickContext


def render_inventory(console: Console, context: SidekickContext) -> None:
    """Render stable local machine metadata without changing state."""
    info = context.platform.info()
    table = Table(title="field-sidekick inventory")
    table.add_column("Item")
    table.add_column("Value")
    table.add_row("System", f"{info.system} {info.release}")
    table.add_row("Machine", info.machine or "unknown")
    table.add_row("Python", info.python_version)
    table.add_row("Profile", context.profile.name)
    table.add_row("Wi-Fi", ", ".join(context.platform.wifi_interfaces()) or "none detected")
    console.print(table)
