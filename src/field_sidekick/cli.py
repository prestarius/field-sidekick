"""Command-line interface for field-sidekick."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.pretty import Pretty

from field_sidekick.config import default_profile_path, load_profile
from field_sidekick.core.platform import current_platform
from field_sidekick.core.runner import CommandRunner
from field_sidekick.doctor import exit_code, render_doctor
from field_sidekick.inventory import render_inventory
from field_sidekick.modules import build_registry

app = typer.Typer(
    name="field",
    help="Declarative field-workstation management and security-engineering toolkit.",
    no_args_is_help=True,
)
modules_app = typer.Typer(help="Inspect field-sidekick modules.")
config_app = typer.Typer(help="Inspect desired-state configuration.")
app.add_typer(modules_app, name="modules")
app.add_typer(config_app, name="config")
console = Console()
DEFAULT_PROFILE_PATH = default_profile_path()


def _context(profile_path: Path):
    profile = load_profile(profile_path)
    platform = current_platform()
    runner = CommandRunner()
    registry = build_registry(profile, runner, platform)
    return profile, platform, registry


@app.command()
def doctor(
    module: Annotated[
        str | None,
        typer.Argument(help="Optional module: system, dev, network, wireless"),
    ] = None,
    profile_path: Annotated[
        Path,
        typer.Option("--profile", exists=True, readable=True),
    ] = DEFAULT_PROFILE_PATH,
) -> None:
    """Run local, non-destructive workstation checks."""
    _, _, registry = _context(profile_path)

    if module and module not in registry.names():
        raise typer.BadParameter(f"Unknown or disabled module: {module}")

    results = render_doctor(console, registry, module)
    if exit_code(results):
        raise typer.Exit(code=1)


@app.command()
def inventory(
    profile_path: Annotated[
        Path,
        typer.Option("--profile", exists=True, readable=True),
    ] = DEFAULT_PROFILE_PATH,
) -> None:
    """Print a concise local machine and enabled-module summary."""
    _, platform, registry = _context(profile_path)
    render_inventory(console, platform, registry)


@modules_app.command("list")
def modules_list(
    profile_path: Annotated[
        Path,
        typer.Option("--profile", exists=True, readable=True),
    ] = DEFAULT_PROFILE_PATH,
) -> None:
    """List implemented modules enabled by the selected profile."""
    profile, platform, registry = _context(profile_path)
    console.print(f"[bold]{profile.profile}[/bold] ({platform.system})")

    for name in registry.names():
        module = registry.get(name)
        console.print(f"• [cyan]{name}[/cyan] — {module.description}")


@config_app.command("show")
def config_show(
    profile_path: Annotated[
        Path,
        typer.Option("--profile", exists=True, readable=True),
    ] = DEFAULT_PROFILE_PATH,
) -> None:
    """Show the validated desired-state profile."""
    profile = load_profile(profile_path)
    console.print(Pretty(profile.model_dump(mode="json")))


if __name__ == "__main__":
    app()
