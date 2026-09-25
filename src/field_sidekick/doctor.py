"""Doctor aggregation and rendering."""

from collections.abc import Iterable

from rich.console import Console
from rich.table import Table

from field_sidekick.core.models import CheckResult, CheckStatus
from field_sidekick.core.registry import ModuleRegistry

_STATUS_STYLE = {
    CheckStatus.PASS: "green",
    CheckStatus.WARN: "yellow",
    CheckStatus.FAIL: "red",
    CheckStatus.SKIP: "dim",
}


def collect_results(
    registry: ModuleRegistry,
    module_name: str | None = None,
) -> list[CheckResult]:
    modules = [registry.get(module_name)] if module_name else registry.all()
    return [check.run() for module in modules for check in module.checks()]


def exit_code(results: Iterable[CheckResult]) -> int:
    return 1 if any(result.status == CheckStatus.FAIL for result in results) else 0


def render_doctor(
    console: Console,
    registry: ModuleRegistry,
    module_name: str | None = None,
) -> list[CheckResult]:
    results = collect_results(registry, module_name)

    table = Table(title=f"field doctor{f' {module_name}' if module_name else ''}")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")

    for result in results:
        style = _STATUS_STYLE[result.status]
        table.add_row(
            result.title,
            f"[{style}]{result.status}[/{style}]",
            result.detail,
        )

    console.print(table)

    counts = {status: sum(result.status == status for result in results) for status in CheckStatus}
    console.print(
        f"[dim]PASS {counts[CheckStatus.PASS]} · "
        f"WARN {counts[CheckStatus.WARN]} · "
        f"FAIL {counts[CheckStatus.FAIL]} · "
        f"SKIP {counts[CheckStatus.SKIP]}[/dim]"
    )

    return results
