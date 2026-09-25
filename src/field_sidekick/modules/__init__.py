"""Built-in field-sidekick modules."""

from field_sidekick.core.config import ProfileConfig
from field_sidekick.core.platform import PlatformInfo
from field_sidekick.core.registry import ModuleRegistry
from field_sidekick.core.runner import CommandRunner
from field_sidekick.modules.dev import DevModule
from field_sidekick.modules.network import NetworkModule
from field_sidekick.modules.system import SystemModule
from field_sidekick.modules.wireless import WirelessModule


def build_registry(
    profile: ProfileConfig,
    runner: CommandRunner,
    platform: PlatformInfo,
) -> ModuleRegistry:
    implementations = [SystemModule, DevModule, NetworkModule, WirelessModule]
    modules = [
        module_type(runner, platform, profile.module(module_type.name))
        for module_type in implementations
        if profile.module(module_type.name).enabled
    ]
    return ModuleRegistry(modules)


__all__ = ["build_registry"]
