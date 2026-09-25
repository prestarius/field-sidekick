from field_sidekick.core.config import ModuleConfig
from field_sidekick.core.platform import PlatformInfo
from field_sidekick.core.runner import CommandResult
from field_sidekick.modules.dev import DevModule
from field_sidekick.modules.system import SystemModule
from field_sidekick.modules.wireless import WirelessModule


class FakeRunner:
    def __init__(
        self,
        binaries: dict[str, str] | None = None,
        results: dict[tuple[str, ...], CommandResult] | None = None,
    ) -> None:
        self.binaries = binaries or {}
        self.results = results or {}

    def which(self, command: str) -> str | None:
        return self.binaries.get(command)

    def run(self, *args: str, timeout: float = 3.0) -> CommandResult:
        return self.results.get(
            tuple(args),
            CommandResult(127, stderr="not mocked"),
        )


def kali() -> PlatformInfo:
    return PlatformInfo("Linux", "6.12", "x86_64", {"ID": "kali"})


def mac() -> PlatformInfo:
    return PlatformInfo("Darwin", "25.0", "arm64", {})


def test_system_module_recognizes_kali() -> None:
    result = SystemModule(FakeRunner(), kali()).checks()[0].run()  # type: ignore[arg-type]
    assert result.status.value == "PASS"


def test_system_module_handles_macos_as_warning() -> None:
    result = SystemModule(FakeRunner(), mac()).checks()[0].run()  # type: ignore[arg-type]
    assert result.status.value == "WARN"


def test_dev_module_reports_docker_daemon() -> None:
    runner = FakeRunner(
        binaries={
            "git": "/usr/bin/git",
            "uv": "/usr/bin/uv",
            "docker": "/usr/bin/docker",
        },
        results={
            ("docker", "info", "--format", "{{.ServerVersion}}"): CommandResult(
                0,
                "28.0",
            )
        },
    )
    results = [
        check.run()
        for check in DevModule(runner, kali()).checks()  # type: ignore[arg-type]
    ]
    daemon = next(result for result in results if result.key == "dev.docker-daemon")
    assert daemon.status.value == "PASS"


def test_wireless_skips_linux_specific_checks_on_macos() -> None:
    module = WirelessModule(
        FakeRunner(),
        mac(),
        ModuleConfig(settings={"chipset": "MT7612U"}),
    )  # type: ignore[arg-type]
    results = [check.run() for check in module.checks()]
    assert results[0].status.value == "SKIP"
    assert results[1].status.value == "SKIP"
