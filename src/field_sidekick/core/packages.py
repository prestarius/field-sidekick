"""Small package and service boundary; apt/systemd are implementation details."""

from typing import Protocol

from field_sidekick.core.models import SidekickContext


class PackageManager(Protocol):
    def supported(self, context: SidekickContext) -> bool: ...

    def present(self, context: SidekickContext, package: str) -> bool: ...

    def install(self, context: SidekickContext, package: str) -> bool: ...


class ServiceManager(Protocol):
    def supported(self, context: SidekickContext) -> bool: ...

    def enabled(self, context: SidekickContext, service: str) -> bool: ...

    def enable(self, context: SidekickContext, service: str) -> bool: ...


class AptPackageManager:
    """Kali/Debian package adapter. It is only invoked by explicit apply."""

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


class SystemdServiceManager:
    """Linux systemd service adapter with a safe unsupported-platform fallback."""

    def supported(self, context: SidekickContext) -> bool:
        return context.platform.info().system == "Linux" and bool(context.runner.which("systemctl"))

    def enabled(self, context: SidekickContext, service: str) -> bool:
        return context.runner.run(["systemctl", "is-enabled", service]).ok

    def enable(self, context: SidekickContext, service: str) -> bool:
        return context.runner.run(
            ["sudo", "systemctl", "enable", "--now", service], timeout=30.0
        ).ok
