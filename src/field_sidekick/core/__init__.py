"""Small, explicit primitives shared by Field Sidekick modules."""

from field_sidekick.core.models import (
    Check,
    CheckResult,
    CheckStatus,
    SidekickContext,
    SidekickModule,
)
from field_sidekick.core.packages import AptPackageManager, SystemdServiceManager
from field_sidekick.core.platform import LocalPlatform, PlatformInfo
from field_sidekick.core.runner import CommandResult, CommandRunner

__all__ = [
    "Check",
    "CheckResult",
    "CheckStatus",
    "CommandResult",
    "CommandRunner",
    "LocalPlatform",
    "PlatformInfo",
    "SidekickContext",
    "SidekickModule",
    "AptPackageManager",
    "SystemdServiceManager",
]
