"""Wireless adapter checks."""

from pathlib import Path

from field_sidekick.core.models import Check, CheckResult, CheckStatus
from field_sidekick.core.module import SidekickModule


class WirelessModule(SidekickModule):
    name = "wireless"
    description = "Local Wi-Fi interface and adapter visibility"

    def checks(self) -> list[Check]:
        return [
            Check("wireless.interfaces", "Wi-Fi interfaces", self._interfaces),
            Check("wireless.target-adapter", "Configured field adapter", self._target_adapter),
            Check("wireless.iw", "iw tooling", self._iw),
        ]

    def _linux_wifi_interfaces(self) -> list[str]:
        root = Path("/sys/class/net")
        if not root.is_dir():
            return []

        return sorted(
            item.name
            for item in root.iterdir()
            if (item / "wireless").exists() or item.name.startswith(("wl", "wlan"))
        )

    def _interfaces(self) -> CheckResult:
        if not self.platform.is_linux:
            return CheckResult(
                "wireless.interfaces",
                "Wi-Fi interfaces",
                CheckStatus.SKIP,
                "Linux wireless inspection is only evaluated on the Kali target",
            )

        names = self._linux_wifi_interfaces()
        return CheckResult(
            "wireless.interfaces",
            "Wi-Fi interfaces",
            CheckStatus.PASS if names else CheckStatus.WARN,
            ", ".join(names) or "none detected",
        )

    def _target_adapter(self) -> CheckResult:
        expected = str(self.config.settings.get("chipset", "MT7612U"))

        if not self.platform.is_linux:
            return CheckResult(
                "wireless.target-adapter",
                "Configured field adapter",
                CheckStatus.SKIP,
                f"expected {expected}; not checked off Linux",
            )

        if not self.runner.which("lsusb"):
            return CheckResult(
                "wireless.target-adapter",
                "Configured field adapter",
                CheckStatus.SKIP,
                "lsusb unavailable",
            )

        result = self.runner.run("lsusb")
        needles = [expected.lower(), "mt7612", "awus036acm", "alfa"]
        found = next(
            (
                line
                for line in result.stdout.splitlines()
                if any(needle in line.lower() for needle in needles)
            ),
            "",
        )

        return CheckResult(
            "wireless.target-adapter",
            "Configured field adapter",
            CheckStatus.PASS if found else CheckStatus.WARN,
            found or f"{expected} / Alfa AWUS036ACM not detected",
        )

    def _iw(self) -> CheckResult:
        path = self.runner.which("iw")
        return CheckResult(
            "wireless.iw",
            "iw tooling",
            CheckStatus.PASS if path else CheckStatus.WARN,
            path or "iw not found",
        )
