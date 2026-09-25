"""System checks."""

import platform as py_platform

from field_sidekick.core.models import Check, CheckResult, CheckStatus
from field_sidekick.core.module import SidekickModule


class SystemModule(SidekickModule):
    name = "system"
    description = "Operating system and Python runtime"

    def checks(self) -> list[Check]:
        return [
            Check("system.os", "Operating system", self._os),
            Check("system.python", "Python", self._python),
        ]

    def _os(self) -> CheckResult:
        if self.platform.distro_id == "kali":
            status = CheckStatus.PASS
            detail = f"Kali Linux {self.platform.release}"
        elif self.platform.is_linux:
            status = CheckStatus.WARN
            detail = (
                f"Linux ({self.platform.distro_id or 'unknown distro'}) "
                f"{self.platform.release}"
            )
        elif self.platform.is_macos:
            status = CheckStatus.WARN
            detail = (
                f"macOS {self.platform.release}; supported for development, "
                "Kali is the target"
            )
        else:
            status = CheckStatus.WARN
            detail = f"{self.platform.system} {self.platform.release}; Kali is the target"

        return CheckResult("system.os", "Operating system", status, detail)

    def _python(self) -> CheckResult:
        version = tuple(map(int, py_platform.python_version_tuple()[:2]))
        status = CheckStatus.PASS if version >= (3, 13) else CheckStatus.FAIL
        return CheckResult(
            "system.python",
            "Python",
            status,
            f"{py_platform.python_version()} (requires >=3.13)",
        )
