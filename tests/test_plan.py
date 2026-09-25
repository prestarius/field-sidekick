from dataclasses import dataclass
from pathlib import Path

from field_sidekick.config import (
    Component,
    FirefoxProfileSpec,
    PackageSpec,
    Profile,
    PythonToolSpec,
    ServiceSpec,
)
from field_sidekick.core import PlatformInfo, SidekickContext
from field_sidekick.plan import PlanAction, PlanStatus, Providers, apply_plan, build_plan
from field_sidekick.providers import FirefoxProfileProvider, ManualProvider, ServiceState


class FakeApt:
    def __init__(self, installed: set[str] | None = None) -> None:
        self.installed = installed or set()
        self.calls: list[str] = []

    def supported(self, context: SidekickContext) -> bool:
        return True

    def present(self, context: SidekickContext, name: str) -> bool:
        return name in self.installed

    def install(self, context: SidekickContext, name: str) -> bool:
        self.calls.append(name)
        self.installed.add(name)
        return True


class FakeService:
    def __init__(self) -> None:
        self.states: dict[str, ServiceState] = {}
        self.calls: list[str] = []

    def supported(self, context: SidekickContext) -> bool:
        return True

    def state(self, context: SidekickContext, name: str) -> ServiceState:
        return self.states.get(name, ServiceState(False, False))

    def enable(self, context: SidekickContext, name: str) -> bool:
        self.calls.append(name)
        self.states[name] = ServiceState(True, True)
        return True


@dataclass
class FakePlatform:
    def info(self) -> PlatformInfo:
        return PlatformInfo("Linux", "1", "x86_64", "3.13.0")


def context() -> SidekickContext:
    component = Component(
        name="dev",
        packages=[PackageSpec(name="git")],
        python_tools=[PythonToolSpec(name="esptool")],
        services=[
            ServiceSpec(name="docker.service"),
            ServiceSpec(name="syncthing.service", scope="user"),
        ],
        firefox_profiles=[FirefoxProfileSpec(name="ai")],
        capabilities=["vendor app"],
    )
    return SidekickContext(Profile(name="test", components=[component]), object(), FakePlatform())


def test_plan_reports_provider_states_and_manual(tmp_path: Path) -> None:
    apt, tools, system, user = FakeApt({"git"}), FakeApt(), FakeService(), FakeService()
    providers = Providers(
        apt, tools, system, user, FirefoxProfileProvider(tmp_path), ManualProvider()
    )
    items = build_plan(context(), providers=providers)
    assert [item.status for item in items] == [
        PlanStatus.OK,
        PlanStatus.MISSING,
        PlanStatus.CHANGE,
        PlanStatus.CHANGE,
        PlanStatus.MISSING,
        PlanStatus.CHANGE,
        PlanStatus.MANUAL,
    ]
    assert {item.provider for item in items} >= {
        "apt",
        "uv-tool",
        "systemd",
        "systemd-user",
        "firefox",
        "manual",
    }


def test_dry_run_and_idempotent_apply(tmp_path: Path) -> None:
    apt, tools, system, user = FakeApt({"git"}), FakeApt(), FakeService(), FakeService()
    firefox = FirefoxProfileProvider(tmp_path)
    providers = Providers(apt, tools, system, user, firefox, ManualProvider())
    items = build_plan(context(), providers=providers)
    apply_plan(context(), items, providers, dry_run=True)
    assert not apt.calls and not tools.calls and not system.calls and not user.calls
    apply_plan(context(), items, providers)
    assert tools.calls == ["esptool"]
    assert system.calls == ["docker.service"]
    assert user.calls == ["syncthing.service"]
    assert firefox.preferences_managed("ai")
    next_items = build_plan(context(), providers=providers)
    assert all(item.action is PlanAction.NONE for item in next_items)
