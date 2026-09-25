"""Passive local network-configuration checks."""

from field_sidekick.core import Check, CheckResult, CheckStatus, SidekickContext, SidekickModule


class NetworkModule(SidekickModule):
    name = "network"
    description = "Local interfaces, default route, and DNS configuration"

    def checks(self, context: SidekickContext) -> tuple[Check, ...]:
        return (
            Check("Interfaces", self._interfaces),
            Check("Default route", self._route),
            Check("DNS", self._dns),
        )

    def _interfaces(self, context: SidekickContext) -> CheckResult:
        command = ["ip", "-brief", "address"] if context.runner.which("ip") else ["ifconfig", "-l"]
        result = context.runner.run(command)
        status = CheckStatus.PASS if result.ok and result.stdout else CheckStatus.WARN
        return CheckResult(
            self.name, "Interfaces", status, result.stdout or "no local interface data available"
        )

    def _route(self, context: SidekickContext) -> CheckResult:
        command = (
            ["ip", "route", "show", "default"]
            if context.runner.which("ip")
            else ["route", "-n", "get", "default"]
        )
        result = context.runner.run(command)
        status = CheckStatus.PASS if result.ok and result.stdout else CheckStatus.WARN
        return CheckResult(
            self.name, "Default route", status, result.stdout or "no default route reported"
        )

    def _dns(self, context: SidekickContext) -> CheckResult:
        resolv = context.platform.read_text("/etc/resolv.conf")
        if resolv is None:
            return CheckResult(
                self.name, "DNS", CheckStatus.SKIP, "no /etc/resolv.conf on this platform"
            )
        servers = [
            line.split(maxsplit=1)[1]
            for line in resolv.splitlines()
            if line.startswith("nameserver ")
        ]
        status = CheckStatus.PASS if servers else CheckStatus.WARN
        return CheckResult(
            self.name, "DNS", status, ", ".join(servers) or "no nameserver configured"
        )
