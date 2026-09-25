"""Explicit local-state providers used by the planner; not a plugin framework."""

from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

from field_sidekick.core.models import SidekickContext


@dataclass(frozen=True)
class ServiceState:
    enabled: bool
    running: bool


class AptProvider:
    """Kali/Debian apt package provider, used only after explicit confirmation."""

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux" and bool(
            context.runner.which("dpkg-query")
        )

    def present(self, context: SidekickContext, package: str) -> bool:
        result = context.runner.run(["dpkg-query", "-W", "-f=${db:Status-Status}", package])
        return result.ok and result.stdout == "installed"

    def install(self, context: SidekickContext, package: str) -> bool:
        return context.runner.run(
            ["sudo", "apt-get", "install", "--yes", package], timeout=120.0
        ).ok


class UvToolProvider:
    """Install Python CLIs with ``uv tool``; libraries without CLIs remain manual."""

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux" and bool(context.runner.which("uv"))

    def present(self, context: SidekickContext, package: str) -> bool:
        result = context.runner.run(["uv", "tool", "list"], timeout=15.0)
        return result.ok and any(
            line.split(maxsplit=1)[0] == package for line in result.stdout.splitlines()
        )

    def install(self, context: SidekickContext, package: str) -> bool:
        return context.runner.run(["uv", "tool", "install", package], timeout=180.0).ok


class SystemdServiceProvider:
    """System-level systemd service provider."""

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux" and bool(context.runner.which("systemctl"))

    def state(self, context: SidekickContext, service: str) -> ServiceState:
        return ServiceState(
            enabled=context.runner.run(["systemctl", "is-enabled", service]).ok,
            running=context.runner.run(["systemctl", "is-active", service]).ok,
        )

    def enable(self, context: SidekickContext, service: str) -> bool:
        return context.runner.run(
            ["sudo", "systemctl", "enable", "--now", service], timeout=30.0
        ).ok


class SystemdUserServiceProvider:
    """Per-user systemd service provider; never uses sudo."""

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux" and bool(context.runner.which("systemctl"))

    def state(self, context: SidekickContext, service: str) -> ServiceState:
        args = ["systemctl", "--user"]
        return ServiceState(
            enabled=context.runner.run([*args, "is-enabled", service]).ok,
            running=context.runner.run([*args, "is-active", service]).ok,
        )

    def enable(self, context: SidekickContext, service: str) -> bool:
        return context.runner.run(
            ["systemctl", "--user", "enable", "--now", service], timeout=30.0
        ).ok


FIREFOX_PREFERENCES = {
    "signon.rememberSignons": False,
    "extensions.formautofill.addresses.enabled": False,
    "extensions.formautofill.creditCards.enabled": False,
}
PREFS_START = "// field-sidekick managed preferences: start"
PREFS_END = "// field-sidekick managed preferences: end"


def render_firefox_preferences() -> str:
    """Return a stable, narrow user.js block without unrelated browser settings."""
    lines = [PREFS_START]
    lines.extend(
        f'user_pref("{key}", {str(value).lower()});' for key, value in FIREFOX_PREFERENCES.items()
    )
    lines.append(PREFS_END)
    return "\n".join(lines) + "\n"


class FirefoxProfileProvider:
    """Manage only named dedicated profiles; existing data is never overwritten."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.home() / ".mozilla" / "firefox"

    @property
    def ini_path(self) -> Path:
        return self.root / "profiles.ini"

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux"

    def _profiles(self) -> dict[str, Path]:
        parser = configparser.RawConfigParser()
        if self.ini_path.exists():
            parser.read(self.ini_path, encoding="utf-8")
        profiles: dict[str, Path] = {}
        for section in parser.sections():
            if section.startswith("Profile"):
                name = parser.get(section, "Name", fallback="")
                relative = parser.getboolean(section, "IsRelative", fallback=True)
                path = Path(parser.get(section, "Path", fallback=""))
                if name and path:
                    profiles[name] = self.root / path if relative else path
        return profiles

    def profile_path(self, name: str) -> Path | None:
        return self._profiles().get(name)

    def exists(self, name: str) -> bool:
        return self.profile_path(name) is not None

    def preferences_managed(self, name: str) -> bool:
        path = self.profile_path(name)
        if path is None:
            return False
        try:
            content = (path / "user.js").read_text(encoding="utf-8")
        except OSError:
            return False
        return all(f'user_pref("{key}", false);' in content for key in FIREFOX_PREFERENCES)

    def create(self, name: str) -> bool:
        if self.exists(name):
            return True
        self.root.mkdir(parents=True, exist_ok=True)
        directory = f"field-sidekick.{name}"
        profile_path = self.root / directory
        if profile_path.exists():
            return False
        profile_path.mkdir()
        parser = configparser.RawConfigParser()
        if self.ini_path.exists():
            parser.read(self.ini_path, encoding="utf-8")
        index = 0
        while parser.has_section(f"Profile{index}"):
            index += 1
        section = f"Profile{index}"
        parser.add_section(section)
        parser.set(section, "Name", name)
        parser.set(section, "IsRelative", "1")
        parser.set(section, "Path", directory)
        with self.ini_path.open("w", encoding="utf-8") as handle:
            parser.write(handle)
        return True

    def configure_preferences(self, name: str) -> bool:
        profile_path = self.profile_path(name)
        if profile_path is None:
            return False
        target = profile_path / "user.js"
        try:
            existing = target.read_text(encoding="utf-8")
        except FileNotFoundError:
            existing = ""
        start, end = existing.find(PREFS_START), existing.find(PREFS_END)
        if start >= 0 and end >= start:
            end += len(PREFS_END)
            content = existing[:start] + render_firefox_preferences().rstrip() + existing[end:]
        else:
            content = (
                existing.rstrip()
                + ("\n\n" if existing.strip() else "")
                + render_firefox_preferences()
            )
        target.write_text(content, encoding="utf-8")
        return True


class ManualProvider:
    """Detection only for intentional manual/vendor/account-bound capabilities."""

    def present(self, context: SidekickContext, command: str | None) -> bool | None:
        return bool(context.runner.which(command)) if command else None
