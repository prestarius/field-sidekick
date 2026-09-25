"""Local networking checks."""

from pathlib import Path

from field_sidekick.core.models import Check, CheckResult, CheckStatus
from field_sidekick.core.module import SidekickModule


class NetworkModule(SidekickModule):
    name = "network"
    description = "Local interfaces, route and resolver visibility"

    def checks(self) -> list[Check]:
        return [
            Check("network.interfaces", "Network interfaces", self._interfaces),
            Check("network.default-route", "Default route", self._default_route),
            Check("network.dns", "DNS resolver", self._dns),
        ]

    def _interfaces(self) -> CheckResult:
        path = Path("/sys/class/net")
        if path.is_dir():
            names = sorted(item.name for item in path.iterdir() if item.name != "lo")
            return CheckResult(
                "network.interfaces",
                "Network interfaces",
                CheckStatus.PASS if names else CheckStatus.WARN,
                ", ".join(names) or "none",
            )

        if self.platform.is_macos and self.runner.which("ifconfig"):
            result = self.runner.run("ifconfig", "-l")
            names = (
                [name for name in result.stdout.split() if name != "lo0"]
                if result.ok
                else []
            )
            return CheckResult(
                "network.interfaces",
                "Network interfaces",
                CheckStatus.PASS if names else CheckStatus.WARN,
                ", ".join(names) or "none detected",
            )

        return CheckResult(
            "network.interfaces",
            "Network interfaces",
            CheckStatus.SKIP,
            "interface enumeration unavailable",
        )

    def _default_route(self) -> CheckResult:
        if self.runner.which("ip"):
            result = self.runner.run("ip", "route", "show", "default")
        elif self.platform.is_macos and self.runner.which("route"):
            result = self.runner.run("route", "-n", "get", "default")
        else:
            return CheckResult(
                "network.default-route",
                "Default route",
                CheckStatus.SKIP,
                "no supported route command",
            )

        detail = (
            result.stdout.splitlines()[0]
            if result.stdout
            else (result.stderr or "not found")
        )
        return CheckResult(
            "network.default-route",
            "Default route",
            CheckStatus.PASS if result.ok and result.stdout else CheckStatus.WARN,
            detail,
        )

    def _dns(self) -> CheckResult:
        resolv = Path("/etc/resolv.conf")
        if not resolv.is_file():
            return CheckResult(
                "network.dns",
                "DNS resolver",
                CheckStatus.SKIP,
                "resolver data unavailable",
            )

        servers = [
            line.split()[1]
            for line in resolv.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.startswith("nameserver ") and len(line.split()) >= 2
        ]
        return CheckResult(
            "network.dns",
            "DNS resolver",
            CheckStatus.PASS if servers else CheckStatus.WARN,
            ", ".join(servers) or "no nameserver entries",
        )
