from dataclasses import dataclass

import pytest

from field_sidekick.config import ModuleConfig, Profile
from field_sidekick.core import (
    CheckResult,
    CheckStatus,
    CommandResult,
    PlatformInfo,
    SidekickContext,
)
from field_sidekick.core.registry import ModuleRegistry
from field_sidekick.doctor import collect_results, has_failures
from field_sidekick.modules.dev import DevModule
from field_sidekick.modules.system import SystemModule
from field_sidekick.modules.wireless import WirelessModule


class FakeRunner:
    def __init__(self, commands: set[str] | None = None, output: str = "", code: int = 0) -> None:
        self.commands, self.output, self.code = commands or set(), output, code

    def which(self, command: str) -> str | None:
        return f"/bin/{command}" if command in self.commands else None

    def run(self, args: list[str]) -> CommandResult:
        return CommandResult(self.code, self.output)


@dataclass
class FakePlatform:
    platform_info: PlatformInfo
    text: str | None = None
    wifi: list[str] | None = None

    def info(self) -> PlatformInfo:
        return self.platform_info

    def read_text(self, path: str) -> str | None:
        return self.text

    def wifi_interfaces(self) -> list[str]:
        return self.wifi or []


def context(
    system: str = "Linux",
    version: str = "3.13.1",
    commands: set[str] | None = None,
    output: str = "",
) -> SidekickContext:
    profile = Profile(
        name="test",
        modules={"system": ModuleConfig(), "dev": ModuleConfig(), "wireless": ModuleConfig()},
    )
    return SidekickContext(
        profile,
        FakeRunner(commands, output),
        FakePlatform(PlatformInfo(system, "1", "x86_64", version), "ID=kali", ["wlan1"]),
    )


def test_dev_reports_docker_daemon_and_python() -> None:
    results = DevModule().run(context(commands={"git", "uv", "docker"}, output="27.0"))
    assert {result.status for result in results} == {CheckStatus.PASS}
    assert "daemon reachable" in results[-1].detail


def test_macos_wireless_checks_skip_gracefully() -> None:
    results = WirelessModule().run(context(system="Darwin"))
    assert [result.status for result in results] == [CheckStatus.SKIP, CheckStatus.SKIP]


def test_system_detects_kali_and_registry_honors_disabled_module() -> None:
    ctx = context()
    assert all(result.status is CheckStatus.PASS for result in SystemModule().run(ctx))
    ctx.profile.modules["dev"].enabled = False
    registry = ModuleRegistry([SystemModule(), DevModule()])
    assert [result.module for result in collect_results(registry, ctx)] == ["system", "system"]


def test_registry_duplicate_unknown_and_failure_aggregation() -> None:
    registry = ModuleRegistry([SystemModule()])
    with pytest.raises(ValueError, match="already registered"):
        registry.register(SystemModule())
    with pytest.raises(ValueError, match="Unknown module"):
        registry.get("missing")
    failures = [CheckResult("x", "x", CheckStatus.FAIL, "x")]
    assert has_failures(failures)
