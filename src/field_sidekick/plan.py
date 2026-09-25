"""Read-only desired-state planning and explicit provider-backed application."""

from dataclasses import dataclass
from enum import StrEnum

from rich.console import Console
from rich.table import Table

from field_sidekick.core import SidekickContext
from field_sidekick.providers import (
    AptProvider,
    FirefoxProfileProvider,
    ManualProvider,
    SystemdServiceProvider,
    SystemdUserServiceProvider,
    UvToolProvider,
)


class PlanStatus(StrEnum):
    OK = "OK"
    MISSING = "MISSING"
    CHANGE = "CHANGE"
    SKIP = "SKIP"
    MANUAL = "MANUAL"


class PlanAction(StrEnum):
    NONE = "NONE"
    INSTALL_APT_PACKAGE = "INSTALL_APT_PACKAGE"
    INSTALL_PYTHON_TOOL = "INSTALL_PYTHON_TOOL"
    ENABLE_SYSTEM_SERVICE = "ENABLE_SYSTEM_SERVICE"
    ENABLE_USER_SERVICE = "ENABLE_USER_SERVICE"
    CREATE_FIREFOX_PROFILE = "CREATE_FIREFOX_PROFILE"
    CONFIGURE_FIREFOX_PREFERENCES = "CONFIGURE_FIREFOX_PREFERENCES"
    INSTALL_PACKAGE = INSTALL_APT_PACKAGE
    ENABLE_SERVICE = ENABLE_SYSTEM_SERVICE


@dataclass(frozen=True)
class PlanItem:
    scope: str
    provider: str
    kind: str
    name: str
    status: PlanStatus
    action: PlanAction
    detail: str


@dataclass(frozen=True)
class Providers:
    apt: AptProvider
    uv_tool: UvToolProvider
    systemd: SystemdServiceProvider
    systemd_user: SystemdUserServiceProvider
    firefox: FirefoxProfileProvider
    manual: ManualProvider


def default_providers() -> Providers:
    return Providers(
        AptProvider(),
        UvToolProvider(),
        SystemdServiceProvider(),
        SystemdUserServiceProvider(),
        FirefoxProfileProvider(),
        ManualProvider(),
    )


def _service_item(
    context: SidekickContext, component: str, service, provider, label: str
) -> PlanItem:
    if not provider.supported(context):
        return PlanItem(
            component,
            label,
            "service",
            service.name,
            PlanStatus.SKIP,
            PlanAction.NONE,
            "systemd is unavailable",
        )
    state = provider.state(context, service.name)
    detail = (
        f"{'enabled' if state.enabled else 'disabled'}; {'running' if state.running else 'stopped'}"
    )
    if state.enabled and state.running:
        return PlanItem(
            component, label, "service", service.name, PlanStatus.OK, PlanAction.NONE, detail
        )
    action = (
        PlanAction.ENABLE_USER_SERVICE
        if label == "systemd-user"
        else PlanAction.ENABLE_SYSTEM_SERVICE
    )
    return PlanItem(component, label, "service", service.name, PlanStatus.CHANGE, action, detail)


def build_plan(
    context: SidekickContext, scope: str | None = None, providers: Providers | None = None
) -> list[PlanItem]:
    """Compare selected declarative components with local state without changing it."""
    providers = providers or default_providers()
    components = context.profile.components
    if scope and scope != "packages":
        components = [component for component in components if component.name == scope]
        if not components:
            raise ValueError(f"Unknown plan scope: {scope}")
    result: list[PlanItem] = []
    for component in components:
        for package in component.packages:
            if not providers.apt.supported(context):
                result.append(
                    PlanItem(
                        component.name,
                        "apt",
                        "package",
                        package.name,
                        PlanStatus.SKIP,
                        PlanAction.NONE,
                        "apt/dpkg is unavailable",
                    )
                )
            elif providers.apt.present(context, package.apt_name):
                result.append(
                    PlanItem(
                        component.name,
                        "apt",
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
                        "apt",
                        "package",
                        package.name,
                        PlanStatus.MISSING,
                        PlanAction.INSTALL_APT_PACKAGE,
                        package.apt_name,
                    )
                )
        for tool in component.python_tools:
            if not providers.uv_tool.supported(context):
                result.append(
                    PlanItem(
                        component.name,
                        "uv-tool",
                        "python-tool",
                        tool.name,
                        PlanStatus.SKIP,
                        PlanAction.NONE,
                        "uv is unavailable",
                    )
                )
            elif providers.uv_tool.present(context, tool.package_name):
                result.append(
                    PlanItem(
                        component.name,
                        "uv-tool",
                        "python-tool",
                        tool.name,
                        PlanStatus.OK,
                        PlanAction.NONE,
                        "installed",
                    )
                )
            else:
                result.append(
                    PlanItem(
                        component.name,
                        "uv-tool",
                        "python-tool",
                        tool.name,
                        PlanStatus.MISSING,
                        PlanAction.INSTALL_PYTHON_TOOL,
                        tool.package_name,
                    )
                )
        for service in component.services:
            provider = providers.systemd_user if service.scope == "user" else providers.systemd
            label = "systemd-user" if service.scope == "user" else "systemd"
            item = _service_item(context, component.name, service, provider, label)
            if not service.managed and item.status is not PlanStatus.SKIP:
                item = PlanItem(
                    item.scope,
                    "manual",
                    item.kind,
                    item.name,
                    PlanStatus.MANUAL,
                    PlanAction.NONE,
                    f"{item.detail}; vendor install, login, and enrollment remain manual",
                )
            elif not service.enabled and item.status is not PlanStatus.SKIP:
                item = PlanItem(
                    item.scope,
                    item.provider,
                    item.kind,
                    item.name,
                    PlanStatus.OK,
                    PlanAction.NONE,
                    item.detail,
                )
            result.append(item)
        for profile in component.firefox_profiles:
            if not providers.firefox.supported(context):
                result.append(
                    PlanItem(
                        component.name,
                        "firefox",
                        "profile",
                        profile.name,
                        PlanStatus.SKIP,
                        PlanAction.NONE,
                        "dedicated Kali profiles require Linux",
                    )
                )
            elif not providers.firefox.exists(profile.name):
                result.append(
                    PlanItem(
                        component.name,
                        "firefox",
                        "profile",
                        profile.name,
                        PlanStatus.MISSING,
                        PlanAction.CREATE_FIREFOX_PROFILE,
                        "create dedicated profile",
                    )
                )
            else:
                result.append(
                    PlanItem(
                        component.name,
                        "firefox",
                        "profile",
                        profile.name,
                        PlanStatus.OK,
                        PlanAction.NONE,
                        "existing dedicated profile",
                    )
                )
            if profile.manage_privacy_preferences:
                if not providers.firefox.supported(context):
                    status, action = PlanStatus.SKIP, PlanAction.NONE
                    detail = "dedicated Kali profiles require Linux"
                else:
                    status = (
                        PlanStatus.OK
                        if providers.firefox.preferences_managed(profile.name)
                        else PlanStatus.CHANGE
                    )
                    action = (
                        PlanAction.NONE
                        if status is PlanStatus.OK
                        else PlanAction.CONFIGURE_FIREFOX_PREFERENCES
                    )
                    detail = "password, address, and payment saving disabled"
                result.append(
                    PlanItem(
                        component.name,
                        "firefox",
                        "config",
                        f"{profile.name} privacy",
                        status,
                        action,
                        detail,
                    )
                )
        for manual in component.manual:
            present = providers.manual.present(context, manual.command)
            state = (
                "present"
                if present
                else "not detected"
                if present is False
                else "not locally detected"
            )
            result.append(
                PlanItem(
                    component.name,
                    "manual",
                    "manual",
                    manual.name,
                    PlanStatus.MANUAL,
                    PlanAction.NONE,
                    f"{state}; {manual.description}",
                )
            )
        result.extend(
            PlanItem(
                component.name,
                "manual",
                "declarative",
                value,
                PlanStatus.MANUAL,
                PlanAction.NONE,
                "user-managed",
            )
            for value in component.capabilities
        )
    return result


def apply_plan(
    context: SidekickContext,
    items: list[PlanItem],
    providers: Providers | None = None,
    dry_run: bool = False,
) -> list[PlanItem]:
    """Apply actionable items only; a fresh plan makes repeat application a no-op."""
    if dry_run:
        return items
    providers = providers or default_providers()
    for item in items:
        if item.action is PlanAction.INSTALL_APT_PACKAGE:
            providers.apt.install(context, item.detail)
        elif item.action is PlanAction.INSTALL_PYTHON_TOOL:
            providers.uv_tool.install(context, item.detail)
        elif item.action is PlanAction.ENABLE_SYSTEM_SERVICE:
            providers.systemd.enable(context, item.name)
        elif item.action is PlanAction.ENABLE_USER_SERVICE:
            providers.systemd_user.enable(context, item.name)
        elif item.action is PlanAction.CREATE_FIREFOX_PROFILE:
            providers.firefox.create(item.name)
        elif item.action is PlanAction.CONFIGURE_FIREFOX_PREFERENCES:
            providers.firefox.configure_preferences(item.name.removesuffix(" privacy"))
    return items


def render_plan(console: Console, items: list[PlanItem], title: str = "field plan") -> None:
    table = Table(title=title)
    for column in ("Scope", "Provider", "Kind", "Name", "Status", "Action", "Detail"):
        table.add_column(column)
    for item in items:
        table.add_row(
            item.scope, item.provider, item.kind, item.name, item.status, item.action, item.detail
        )
    console.print(table)
    summary = "  ".join(
        f"{status}: {sum(item.status is status for item in items)}" for status in PlanStatus
    )
    console.print(f"[dim]{summary or 'No desired state selected.'}[/dim]")
