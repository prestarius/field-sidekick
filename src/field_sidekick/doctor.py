"""Safe, read-only local health checks."""

import platform
import shutil
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table


@dataclass(frozen=True)
class Check:
    name: str
    available: bool
    detail: str


def _command_check(name: str, command: str) -> Check:
    path = shutil.which(command)
    return Check(name, path is not None, path or "not found")


def wifi_interfaces() -> list[str]:
    """Return likely Wi-Fi interfaces based on local Linux interface names."""
    sys_net = Path("/sys/class/net")
    if not sys_net.is_dir():
        return []
    return sorted(
        interface.name
        for interface in sys_net.iterdir()
        if (interface / "wireless").exists() or interface.name.startswith(("wl", "wlan"))
    )


def collect_checks() -> list[Check]:
    """Collect only local, non-mutating state; do not query services or networks."""
    os_detail = f"{platform.system()} {platform.release()}"
    interfaces = wifi_interfaces()
    return [
        Check("Operating system", platform.system() == "Linux", os_detail),
        _command_check("Python", "python3"),
        _command_check("Git", "git"),
        _command_check("Docker", "docker"),
        _command_check("Tailscale", "tailscale"),
        _command_check("Syncthing", "syncthing"),
        Check("Wi-Fi interfaces", bool(interfaces), ", ".join(interfaces) or "none detected"),
    ]


def render_doctor(console: Console) -> None:
    """Render safe local checks in a compact table."""
    table = Table(title="field-sidekick doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for check in collect_checks():
        status = "[green]OK[/green]" if check.available else "[yellow]Not available[/yellow]"
        table.add_row(check.name, status, check.detail)
    console.print(table)
    console.print(
        "[dim]Checks are local and read-only; no services or networks were contacted.[/dim]"
    )
