"""Concise local workstation inventory."""

from rich.console import Console
from rich.table import Table

from field_sidekick.core.platform import PlatformInfo
from field_sidekick.core.registry import ModuleRegistry


def render_inventory(
    console: Console,
    platform: PlatformInfo,
    registry: ModuleRegistry,
) -> None:
    table = Table(title="field-sidekick inventory")
    table.add_column("Item")
    table.add_column("Value")
    table.add_row("System", f"{platform.system} {platform.release}")
    table.add_row("Distribution", platform.distro_id or "n/a")
    table.add_row("Machine", platform.machine)
    table.add_row("Enabled modules", ", ".join(registry.names()) or "none")
    console.print(table)
