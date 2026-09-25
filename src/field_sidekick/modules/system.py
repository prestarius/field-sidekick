"""Host operating-system checks."""

from field_sidekick.core import Check, CheckResult, CheckStatus, SidekickContext, SidekickModule


class SystemModule(SidekickModule):
    name = "system"
    description = "Operating-system and Kali target checks"

    def checks(self, context: SidekickContext) -> tuple[Check, ...]:
        return (Check("Operating system", self._os), Check("Kali Linux", self._kali))

    def _os(self, context: SidekickContext) -> CheckResult:
        info = context.platform.info()
        status = CheckStatus.PASS if info.system == "Linux" else CheckStatus.WARN
        return CheckResult(
            self.name, "Operating system", status, f"{info.system} {info.release} ({info.machine})"
        )

    def _kali(self, context: SidekickContext) -> CheckResult:
        if context.platform.info().system != "Linux":
            return CheckResult(
                self.name, "Kali Linux", CheckStatus.SKIP, "Kali detection is Linux-only"
            )
        release = context.platform.read_text("/etc/os-release") or ""
        status = CheckStatus.PASS if "kali" in release.lower() else CheckStatus.WARN
        detail = (
            "Kali Linux detected" if status is CheckStatus.PASS else "Kali Linux was not identified"
        )
        return CheckResult(self.name, "Kali Linux", status, detail)
