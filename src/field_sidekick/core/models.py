"""Shared check/result models."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum


class CheckStatus(StrEnum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    SKIP = "SKIP"


@dataclass(frozen=True)
class CheckResult:
    key: str
    title: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True)
class Check:
    key: str
    title: str
    probe: Callable[[], CheckResult]

    def run(self) -> CheckResult:
        return self.probe()
