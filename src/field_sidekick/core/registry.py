"""Explicit built-in module registry."""

from field_sidekick.config import Profile
from field_sidekick.core.models import SidekickModule


class ModuleRegistry:
    def __init__(self, modules: list[SidekickModule] | None = None) -> None:
        self._modules: dict[str, SidekickModule] = {}
        for module in modules or []:
            self.register(module)

    def register(self, module: SidekickModule) -> None:
        if module.name in self._modules:
            raise ValueError(f"Module already registered: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> SidekickModule:
        try:
            return self._modules[name]
        except KeyError as error:
            raise ValueError(
                f"Unknown module {name!r}; available: {', '.join(self._modules)}"
            ) from error

    def all(self) -> list[SidekickModule]:
        return list(self._modules.values())

    def enabled(self, profile: Profile) -> list[SidekickModule]:
        return [
            m
            for m in self.all()
            if profile.modules.get(m.name, None) is None or profile.modules[m.name].enabled
        ]
