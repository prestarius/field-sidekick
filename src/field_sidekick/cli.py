"""Command-line interface for the declarative Field Sidekick toolkit."""

from pathlib import Path

import typer
from rich.console import Console

from field_sidekick.config import DEFAULT_PROFILE_PATH, load_profile
from field_sidekick.core import CommandRunner, LocalPlatform, SidekickContext
from field_sidekick.doctor import collect_results, has_failures, render_doctor
from field_sidekick.inventory import render_inventory
from field_sidekick.modules import built_in_registry

app = typer.Typer(
    name="field",
    help="Declarative field-workstation management and security-engineering toolkit.",
    no_args_is_help=True,
)
modules_app = typer.Typer(help="Inspect built-in workstation modules.")
config_app = typer.Typer(help="Inspect declarative workstation profiles.")
app.add_typer(modules_app, name="modules")
app.add_typer(config_app, name="config")
console = Console()
PROFILE_OPTION = typer.Option(DEFAULT_PROFILE_PATH, "--profile", exists=True, readable=True)


def context_for(profile_path: Path) -> SidekickContext:
    return SidekickContext(load_profile(profile_path), CommandRunner(), LocalPlatform())


@app.command()
def doctor(
    module: str | None = typer.Argument(
        None, help="Optional module: system, dev, network, wireless."
    ),
    profile: Path = PROFILE_OPTION,
) -> None:
    """Run local, non-destructive checks against the selected desired-state profile."""
    context = context_for(profile)
    try:
        results = collect_results(built_in_registry(), context, module)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="module") from error
    render_doctor(console, results, f"field doctor{f' {module}' if module else ''}")
    if has_failures(results):
        raise typer.Exit(1)


@app.command()
def inventory(
    profile: Path = PROFILE_OPTION,
) -> None:
    """Print a concise local machine and tool summary."""
    render_inventory(console, context_for(profile))


@modules_app.command("list")
def list_modules() -> None:
    """List the built-in module boundary; no dynamic plugin loading occurs."""
    for module in built_in_registry().all():
        console.print(f"[bold]{module.name}[/bold]  {module.description}")


@config_app.command("show")
def show_config(
    profile: Path = PROFILE_OPTION,
) -> None:
    """Show desired state; this command never applies it."""
    console.print_json(load_profile(profile).model_dump_json(indent=2))


if __name__ == "__main__":
    app()
