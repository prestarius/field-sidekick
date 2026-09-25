"""Passive wireless and Alfa/MT7612U readiness checks."""

from field_sidekick.core import Check, CheckResult, CheckStatus, SidekickContext, SidekickModule


class WirelessModule(SidekickModule):
    name = "wireless"
    description = "Wi-Fi interface, driver, and Alfa MT7612U visibility"

    def checks(self, context: SidekickContext) -> tuple[Check, ...]:
        return (Check("Wi-Fi interfaces", self._interfaces), Check("Alfa MT7612U", self._alfa))

    def _interfaces(self, context: SidekickContext) -> CheckResult:
        if context.platform.info().system != "Linux":
            return CheckResult(
                self.name,
                "Wi-Fi interfaces",
                CheckStatus.SKIP,
                "wireless Linux metadata is unavailable",
            )
        interfaces = context.platform.wifi_interfaces()
        status = CheckStatus.PASS if interfaces else CheckStatus.WARN
        return CheckResult(
            self.name, "Wi-Fi interfaces", status, ", ".join(interfaces) or "none detected"
        )

    def _alfa(self, context: SidekickContext) -> CheckResult:
        if context.platform.info().system != "Linux":
            return CheckResult(
                self.name, "Alfa MT7612U", CheckStatus.SKIP, "USB detection is Linux-only"
            )
        if not context.runner.which("lsusb"):
            return CheckResult(
                self.name, "Alfa MT7612U", CheckStatus.SKIP, "lsusb is not installed"
            )
        result = context.runner.run(["lsusb"])
        found = "mt7612" in result.stdout.lower() or "alfa" in result.stdout.lower()
        return CheckResult(
            self.name,
            "Alfa MT7612U",
            CheckStatus.PASS if found else CheckStatus.WARN,
            "detected" if found else "not detected",
        )
