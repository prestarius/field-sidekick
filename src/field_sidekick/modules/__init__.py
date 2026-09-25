"""Built-in local modules."""

from field_sidekick.core.registry import ModuleRegistry
from field_sidekick.modules.dev import DevModule
from field_sidekick.modules.network import NetworkModule
from field_sidekick.modules.system import SystemModule
from field_sidekick.modules.wireless import WirelessModule


def built_in_registry() -> ModuleRegistry:
    return ModuleRegistry([SystemModule(), DevModule(), NetworkModule(), WirelessModule()])
