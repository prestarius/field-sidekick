"""Read-only desired-state planning and explicit application of plan items."""

from dataclasses import dataclass
from enum import StrEnum

from rich.console import Console
from rich.table import Table

from field_sidekick.core import SidekickContext
from field_sidekick.core.packages import (
    AptPackageManager,
    PackageManager,
    ServiceManager,
    SystemdServiceManager,
)


class PlanStatus(StrEnum):
    OK = "OK"
    MISSING = "MISSING"
    CHANGE = "CHANGE"
    SKIP = "SKIP"


class PlanAction(StrEnum):
    NONE = "NONE"
    INSTALL_PACKAGE = "INSTALL_PACKAGE"
    ENABLE_SERVICE = "ENABLE_SERVICE"


@dataclass(frozen=True)
class PlanItem:
    scope: str
    kind: str
    name: str
    status: PlanStatus
    action: PlanAction
    detail: str


def build_plan(
    context: SidekickContext,
    scope: str | None = None,
    packages: PackageManager | None = None,
    services: ServiceManager | None = None,
) -> list[PlanItem]:
    """Compare the selected declarative components with local state."""
    packages = packages or AptPackageManager()
    services = services or SystemdServiceManager()
    components = context.profile.components
    if scope and scope != "packages":
        components = [component for component in components if component.name == scope]
        if not components:
            raise ValueError(f"Unknown plan scope: {scope}")
    result: list[PlanItem] = []
    for component in components:
        for package in component.packages:
            if not packages.supported(context):
                result.append(
                    PlanItem(
                        component.name,
                        "package",
                        package.name,
                        PlanStatus.SKIP,
                        PlanAction.NONE,
                        "apt/dpkg is unavailable on this platform",
                    )
                )
            elif packages.present(context, package.apt_name):
                result.append(
                    PlanItem(
                        component.name,
                        "package",
                        package.name,
                        PlanStatus.OK,
                        PlanAction.NONE,
                        "installed",
                    )
                )
            else:
                result.append(
                    PlanItem(
                        component.name,
                        "package",
                        package.name,
                        PlanStatus.MISSING,
                        PlanAction.INSTALL_PACKAGE,
                        f"apt package: {package.apt_name}",
                    )
                )
        for service in component.services:
            if not service.enabled:
                continue
            if not services.supported(context):
                result.append(
                    PlanItem(
                        component.name,
                        "service",
                        service.name,
                        PlanStatus.SKIP,
                        PlanAction.NONE,
                        "systemd is unavailable on this platform",
                    )
                )
            elif services.enabled(context, service.name):
                result.append(
                    PlanItem(
                        component.name,
                        "service",
                        service.name,
                        PlanStatus.OK,
                        PlanAction.NONE,
                        "enabled",
                    )
                )
            else:
                result.append(
                    PlanItem(
                        component.name,
                        "service",
                        service.name,
                        PlanStatus.CHANGE,
                        PlanAction.ENABLE_SERVICE,
                        "enable and start service",
                    )
                )
        result.extend(
            PlanItem(
                component.name,
                "capability",
                value,
                PlanStatus.SKIP,
                PlanAction.NONE,
                "declarative-only; user-managed",
            )
            for value in component.capabilities
        )
    return result


def apply_plan(
    context: SidekickContext,
    items: list[PlanItem],
    packages: PackageManager | None = None,
    services: ServiceManager | None = None,
    dry_run: bool = False,
) -> list[PlanItem]:
    """Apply only actionable items. Re-running an unchanged plan is a no-op."""
    if dry_run:
        return items
    packages = packages or AptPackageManager()
    services = services or SystemdServiceManager()
    for item in items:
        if item.action is PlanAction.INSTALL_PACKAGE:
            packages.install(context, item.detail.removeprefix("apt package: "))
        elif item.action is PlanAction.ENABLE_SERVICE:
            services.enable(context, item.name)
    return items


def render_plan(console: Console, items: list[PlanItem], title: str = "field plan") -> None:
    table = Table(title=title)
    table.add_column("Scope")
    table.add_column("Kind")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Action")
    table.add_column("Detail")
    for item in items:
        table.add_row(item.scope, item.kind, item.name, item.status, item.action, item.detail)
    console.print(table)
    summary = "  ".join(
        f"{status}: {sum(item.status is status for item in items)}" for status in PlanStatus
    )
    console.print(f"[dim]{summary or 'No desired state selected.'}[/dim]")
