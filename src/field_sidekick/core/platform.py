"""Platform inspection helpers."""

import platform
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlatformInfo:
    system: str
    release: str
    machine: str
    os_release: dict[str, str]

    @property
    def is_linux(self) -> bool:
        return self.system == "Linux"

    @property
    def is_macos(self) -> bool:
        return self.system == "Darwin"

    @property
    def distro_id(self) -> str | None:
        return self.os_release.get("ID")


def current_platform() -> PlatformInfo:
    data: dict[str, str] = {}
    path = Path("/etc/os-release")

    if path.is_file():
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            data[key] = value.strip().strip('"')

    return PlatformInfo(
        system=platform.system(),
        release=platform.release(),
        machine=platform.machine() or "unknown",
        os_release=data,
    )
