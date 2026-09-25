"""Result and module contracts; intentionally no plugin framework."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from field_sidekick.config import Profile


class CheckStatus(StrEnum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    SKIP = "SKIP"

    @property
    def rich_label(self) -> str:
        colors = {self.PASS: "green", self.WARN: "yellow", self.FAIL: "red", self.SKIP: "dim"}
        return f"[{colors[self]}]{self.value}[/{colors[self]}]"


@dataclass(frozen=True)
class CheckResult:
    module: str
    name: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True)
class Check:
    name: str
    run: Callable[["SidekickContext"], CheckResult]


class Platform(Protocol):
    def info(self): ...
    def read_text(self, path: str) -> str | None: ...
    def wifi_interfaces(self) -> list[str]: ...


@dataclass(frozen=True)
class SidekickContext:
    profile: Profile
    runner: object
    platform: Platform


class SidekickModule:
    name: str
    description: str

    def checks(self, context: SidekickContext) -> tuple[Check, ...]:
        raise NotImplementedError

    def run(self, context: SidekickContext) -> list[CheckResult]:
        return [check.run(context) for check in self.checks(context)]
