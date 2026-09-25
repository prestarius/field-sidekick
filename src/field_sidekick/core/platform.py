"""Local platform facts with graceful non-Linux fallbacks."""

import platform as stdlib_platform
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlatformInfo:
    system: str
    release: str
    machine: str
    python_version: str


class LocalPlatform:
    def info(self) -> PlatformInfo:
        return PlatformInfo(
            stdlib_platform.system(),
            stdlib_platform.release(),
            stdlib_platform.machine(),
            stdlib_platform.python_version(),
        )

    def read_text(self, path: str) -> str | None:
        try:
            return Path(path).read_text(encoding="utf-8")
        except OSError:
            return None

    def wifi_interfaces(self) -> list[str]:
        root = Path("/sys/class/net")
        if not root.is_dir():
            return []
        return sorted(
            item.name
            for item in root.iterdir()
            if (item / "wireless").exists() or item.name.startswith(("wl", "wlan"))
        )
