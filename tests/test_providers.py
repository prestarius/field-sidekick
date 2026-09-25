from dataclasses import dataclass
from pathlib import Path

from field_sidekick.config import Profile
from field_sidekick.core import CommandResult, PlatformInfo, SidekickContext
from field_sidekick.providers import (
    AptProvider,
    FirefoxProfileProvider,
    SystemdServiceProvider,
    SystemdUserServiceProvider,
    UvToolProvider,
    render_firefox_preferences,
)


@dataclass
class Platform:
    def info(self) -> PlatformInfo:
        return PlatformInfo("Linux", "1", "x86_64", "3.13")


class Runner:
    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def which(self, command: str) -> str:
        return f"/usr/bin/{command}"

    def run(self, args: list[str], timeout: float = 3.0) -> CommandResult:
        self.commands.append(args)
        if args[:3] == ["uv", "tool", "list"]:
            return CommandResult(0, "esptool v5.0\n")
        if "is-enabled" in args:
            return CommandResult(0)
        if "is-active" in args:
            return CommandResult(1)
        if args[0] == "dpkg-query":
            return CommandResult(0, "installed")
        return CommandResult(0)


def context(runner: Runner) -> SidekickContext:
    return SidekickContext(Profile(name="test"), runner, Platform())


def test_provider_commands_and_service_state() -> None:
    runner = Runner()
    value = context(runner)
    assert AptProvider().present(value, "git")
    assert UvToolProvider().present(value, "esptool")
    assert SystemdServiceProvider().state(value, "docker.service").enabled
    assert not SystemdServiceProvider().state(value, "docker.service").running
    assert SystemdUserServiceProvider().enable(value, "syncthing.service")
    assert ["systemctl", "--user", "enable", "--now", "syncthing.service"] in runner.commands


def test_firefox_profile_creation_and_preference_rendering_preserve_user_file(
    tmp_path: Path,
) -> None:
    provider = FirefoxProfileProvider(tmp_path)
    assert provider.create("ai")
    path = provider.profile_path("ai")
    assert path is not None
    (path / "user.js").write_text('user_pref("unrelated", true);\n', encoding="utf-8")
    assert provider.configure_preferences("ai")
    content = (path / "user.js").read_text(encoding="utf-8")
    assert 'user_pref("unrelated", true);' in content
    assert content.count("field-sidekick managed preferences: start") == 1
    assert "signon.rememberSignons" in render_firefox_preferences()
