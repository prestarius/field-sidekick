"""Doctor aggregation and Rich rendering."""

from collections.abc import Iterable

from rich.console import Console
from rich.table import Table

from field_sidekick.core import CheckResult, CheckStatus, SidekickContext
from field_sidekick.core.registry import ModuleRegistry


def collect_results(
    registry: ModuleRegistry, context: SidekickContext, module: str | None = None
) -> list[CheckResult]:
    modules = [registry.get(module)] if module else registry.enabled(context.profile)
    return [result for item in modules for result in item.run(context)]


def has_failures(results: Iterable[CheckResult]) -> bool:
    return any(result.status is CheckStatus.FAIL for result in results)


def render_doctor(
    console: Console, results: list[CheckResult], title: str = "field doctor"
) -> None:
    table = Table(title=title)
    table.add_column("Module")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for result in results:
        table.add_row(result.module, result.name, result.status.rich_label, result.detail)
    console.print(table)
    counts = {status: sum(item.status is status for item in results) for status in CheckStatus}
    summary = "  ".join(
        f"{status.value}: {counts[status]}" for status in CheckStatus if counts[status]
    )
    console.print(f"[dim]{summary or 'No checks selected.'}[/dim]")
    console.print("[dim]Checks are local and read-only; desired state is not applied.[/dim]")
