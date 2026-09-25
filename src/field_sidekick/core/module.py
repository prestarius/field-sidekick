"""Module contract."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from field_sidekick.core.config import ModuleConfig
from field_sidekick.core.models import Check
from field_sidekick.core.platform import PlatformInfo
from field_sidekick.core.runner import CommandRunner


class SidekickModule(ABC):
    name: str
    description: str

    def __init__(
        self,
        runner: CommandRunner,
        platform: PlatformInfo,
        config: ModuleConfig | None = None,
    ) -> None:
        self.runner = runner
        self.platform = platform
        self.config = config or ModuleConfig()

    @abstractmethod
    def checks(self) -> Sequence[Check]:
        """Return local, non-destructive checks for this module."""
