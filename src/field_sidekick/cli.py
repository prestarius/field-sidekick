"""Command-line interface for the declarative Field Sidekick toolkit."""

from typing import Annotated

import typer
from rich.console import Console

from field_sidekick import __version__
from field_sidekick.config import (
    copy_bundled_configs,
    load_profile,
    resolve_profile,
    user_config_dir,
)
from field_sidekick.core import CommandRunner, LocalPlatform, SidekickContext
from field_sidekick.doctor import collect_results, has_failures, render_doctor
from field_sidekick.inventory import render_inventory
from field_sidekick.modules import built_in_registry
from field_sidekick.plan import apply_plan, build_plan, render_plan

app = typer.Typer(
    name="field",
    help="Declarative field-workstation management and security-engineering toolkit.",
    no_args_is_help=True,
    invoke_without_command=True,
)
modules_app = typer.Typer(help="Inspect built-in workstation modules.")
config_app = typer.Typer(help="Inspect declarative workstation profiles.")
app.add_typer(modules_app, name="modules")
app.add_typer(config_app, name="config")
console = Console()
PROFILE_OPTION = typer.Option(
    None,
    "--profile",
    help="Profile path or name; names prefer user config over bundled templates.",
)


def profile_for(value: str | None):
    try:
        return resolve_profile(value)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="--profile") from error


def context_for(profile: str | None) -> SidekickContext:
    return SidekickContext(load_profile(profile_for(profile)), CommandRunner(), LocalPlatform())


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", is_eager=True, help="Show the installed field-sidekick version."),
    ] = False,
) -> None:
    """Manage a small, declarative field workstation profile."""
    if version:
        console.print(__version__)
        raise typer.Exit()


@app.command()
def doctor(
    module: str | None = typer.Argument(
        None, help="Optional module: system, dev, network, wireless."
    ),
    profile: str | None = PROFILE_OPTION,
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
    profile: str | None = PROFILE_OPTION,
) -> None:
    """Print a concise local machine and tool summary."""
    render_inventory(console, context_for(profile))


@app.command()
def plan(
    scope: str | None = typer.Argument(None, help="Optional scope: packages, dev, wireless, etc."),
    profile: str | None = PROFILE_OPTION,
) -> None:
    """Preview desired-state differences. This command is always read-only."""
    try:
        render_plan(
            console,
            build_plan(context_for(profile), scope),
            f"field plan{f' {scope}' if scope else ''}",
        )
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="scope") from error


@app.command()
def apply(
    scope: str | None = typer.Argument(None, help="Optional scope: packages, dev, wireless, etc."),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show planned changes without executing."
    ),
    yes: bool = typer.Option(
        False, "--yes", help="Confirm package/service changes without prompting."
    ),
    profile: str | None = PROFILE_OPTION,
) -> None:
    """Apply only reliable package/service actions after explicit confirmation."""
    context = context_for(profile)
    try:
        items = build_plan(context, scope)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="scope") from error
    render_plan(console, items, f"field apply{f' {scope}' if scope else ''}")
    actionable = [item for item in items if item.action != "NONE"]
    if dry_run:
        console.print("[dim]Dry run: no changes were made.[/dim]")
        return
    if not actionable:
        console.print("[dim]Nothing to apply.[/dim]")
        return
    if not yes and not typer.confirm("Apply these workstation changes?"):
        console.print("[yellow]Aborted; no changes were made.[/yellow]")
        raise typer.Exit(1)
    apply_plan(context, actionable)
    console.print("[green]Requested changes applied. Run field plan to verify.[/green]")


@modules_app.command("list")
def list_modules() -> None:
    """List the built-in module boundary; no dynamic plugin loading occurs."""
    for module in built_in_registry().all():
        console.print(f"[bold]{module.name}[/bold]  {module.description}")


@config_app.command("show")
def show_config(
    profile: str | None = PROFILE_OPTION,
) -> None:
    """Show desired state; this command never applies it."""
    console.print_json(load_profile(profile_for(profile)).model_dump_json(indent=2))


@config_app.command("path")
def config_path(profile: str | None = PROFILE_OPTION) -> None:
    """Show the user configuration directory and resolved active profile."""
    console.print(f"User config directory: {user_config_dir()}")
    console.print(f"Active profile: {profile_for(profile)}")


@config_app.command("init")
def config_init(
    force: bool = typer.Option(False, "--force", help="Replace existing starter YAML files."),
) -> None:
    """Copy the bundled X1/Kali starter configuration to the user config directory."""
    destination = user_config_dir()
    copied = copy_bundled_configs(destination, force=force)
    if copied:
        console.print(f"Copied {len(copied)} starter file(s) to {destination}")
    else:
        console.print(f"No files changed in {destination}; use --force to replace starter files.")


@config_app.command("validate")
def validate_config(profile: str | None = PROFILE_OPTION) -> None:
    """Validate the selected profile and component composition without applying it."""
    selected = profile_for(profile)
    try:
        loaded = load_profile(selected)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="--profile") from error
    console.print(f"Valid: {loaded.name} ({selected})")


if __name__ == "__main__":
    app()
