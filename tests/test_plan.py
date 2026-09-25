from dataclasses import dataclass

from field_sidekick.config import Component, PackageSpec, Profile, ServiceSpec
from field_sidekick.core import PlatformInfo, SidekickContext
from field_sidekick.plan import PlanAction, PlanStatus, apply_plan, build_plan


class FakePackages:
    def __init__(self, present: set[str] | None = None, supported: bool = True) -> None:
        self.available = supported
        self.installed = present or set()
        self.calls: list[str] = []

    def supported(self, context: SidekickContext) -> bool:
        return self.available

    def present(self, context: SidekickContext, package: str) -> bool:
        return package in self.installed

    def install(self, context: SidekickContext, package: str) -> bool:
        self.calls.append(package)
        self.installed.add(package)
        return True


class FakeServices:
    def __init__(self, enabled: set[str] | None = None, supported: bool = True) -> None:
        self.available = supported
        self.active = enabled or set()
        self.calls: list[str] = []

    def supported(self, context: SidekickContext) -> bool:
        return self.available

    def enabled(self, context: SidekickContext, service: str) -> bool:
        return service in self.active

    def enable(self, context: SidekickContext, service: str) -> bool:
        self.calls.append(service)
        self.active.add(service)
        return True


@dataclass
class FakePlatform:
    system: str = "Linux"

    def info(self) -> PlatformInfo:
        return PlatformInfo(self.system, "1", "x86_64", "3.13.0")


def context(system: str = "Linux") -> SidekickContext:
    profile = Profile(
        name="test",
        components=[
            Component(
                name="dev",
                packages=[PackageSpec(name="git"), PackageSpec(name="docker.io")],
                services=[ServiceSpec(name="docker.service")],
                capabilities=["uv"],
            ),
            Component(name="wireless", packages=[PackageSpec(name="iw")]),
        ],
    )
    return SidekickContext(profile, object(), FakePlatform(system))


def test_plan_reports_ok_missing_change_and_declarative_skip() -> None:
    items = build_plan(context(), packages=FakePackages({"git"}), services=FakeServices())
    assert [item.status for item in items] == [
        PlanStatus.OK,
        PlanStatus.MISSING,
        PlanStatus.CHANGE,
        PlanStatus.SKIP,
        PlanStatus.MISSING,
    ]
    assert items[1].action is PlanAction.INSTALL_PACKAGE
    assert items[2].action is PlanAction.ENABLE_SERVICE


def test_plan_scope_and_non_linux_skip() -> None:
    packages = FakePackages(supported=False)
    items = build_plan(context("Darwin"), "wireless", packages=packages, services=FakeServices())
    assert len(items) == 1
    assert items[0].status is PlanStatus.SKIP


def test_dry_run_and_idempotent_apply() -> None:
    packages, services = FakePackages({"git"}), FakeServices()
    items = build_plan(context(), packages=packages, services=services)
    apply_plan(context(), items, packages, services, dry_run=True)
    assert packages.calls == services.calls == []
    apply_plan(context(), items, packages, services)
    assert packages.calls == ["docker.io", "iw"]
    assert services.calls == ["docker.service"]
    next_items = build_plan(context(), packages=packages, services=services)
    assert all(item.action is PlanAction.NONE for item in next_items)
