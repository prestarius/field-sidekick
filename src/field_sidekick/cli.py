"""Command-line interface for field-sidekick."""

import typer
from rich.console import Console

from field_sidekick.doctor import render_doctor
from field_sidekick.inventory import render_inventory

app = typer.Typer(
    name="field",
    help="Safe local checks and inventory for a field workstation.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def doctor() -> None:
    """Run safe, local availability checks; never alter the system."""
    render_doctor(console)


@app.command()
def inventory() -> None:
    """Print a concise local machine and tool summary."""
    render_inventory(console)


if __name__ == "__main__":
    app()
