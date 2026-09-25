"""Module registry and selection."""

from collections.abc import Iterable

from field_sidekick.core.module import SidekickModule


class ModuleRegistry:
    def __init__(self, modules: Iterable[SidekickModule] = ()) -> None:
        self._modules: dict[str, SidekickModule] = {}
        for module in modules:
            self.register(module)

    def register(self, module: SidekickModule) -> None:
        if module.name in self._modules:
            raise ValueError(f"Module already registered: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> SidekickModule:
        if name not in self._modules:
            raise KeyError(f"Unknown module: {name}")
        return self._modules[name]

    def names(self) -> list[str]:
        return sorted(self._modules)

    def all(self) -> list[SidekickModule]:
        return [self._modules[name] for name in self.names()]
