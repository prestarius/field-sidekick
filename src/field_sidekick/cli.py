"""Command-line interface for the declarative Field Sidekick toolkit."""

from pathlib import Path

import typer
from rich.console import Console

from field_sidekick.config import DEFAULT_PROFILE_PATH, load_profile
from field_sidekick.core import CommandRunner, LocalPlatform, SidekickContext
from field_sidekick.doctor import collect_results, has_failures, render_doctor
from field_sidekick.inventory import render_inventory
from field_sidekick.modules import built_in_registry
from field_sidekick.plan import apply_plan, build_plan, render_plan

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


@app.command()
def plan(
    scope: str | None = typer.Argument(None, help="Optional scope: packages, dev, wireless, etc."),
    profile: Path = PROFILE_OPTION,
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
    profile: Path = PROFILE_OPTION,
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
    profile: Path = PROFILE_OPTION,
) -> None:
    """Show desired state; this command never applies it."""
    console.print_json(load_profile(profile).model_dump_json(indent=2))


if __name__ == "__main__":
    app()
