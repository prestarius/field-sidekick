from pathlib import Path

import pytest
from pydantic import ValidationError

from field_sidekick.core.config import ModuleConfig, ProfileConfig, load_profile
from field_sidekick.core.models import Check, CheckResult, CheckStatus
from field_sidekick.core.registry import ModuleRegistry
from field_sidekick.core.runner import CommandResult
from field_sidekick.doctor import exit_code


def test_check_runs_probe() -> None:
    expected = CheckResult("x", "X", CheckStatus.PASS, "ok")
    assert Check("x", "X", lambda: expected).run() == expected


def test_exit_code_fails_only_on_fail() -> None:
    assert exit_code([CheckResult("x", "X", CheckStatus.WARN, "meh")]) == 0
    assert exit_code([CheckResult("x", "X", CheckStatus.FAIL, "bad")]) == 1


def test_profile_rejects_unknown_top_level_fields(tmp_path: Path) -> None:
    path = tmp_path / "profile.yaml"
    path.write_text("profile: test\nunknown: true\n", encoding="utf-8")

    with pytest.raises(ValidationError):
        load_profile(path)


def test_profile_returns_disabled_config_for_unknown_module() -> None:
    profile = ProfileConfig(
        profile="test",
        modules={"system": ModuleConfig(enabled=True)},
    )
    assert profile.module("system").enabled
    assert not profile.module("missing").enabled


class DummyModule:
    name = "dummy"


def test_registry_rejects_duplicates() -> None:
    registry = ModuleRegistry()
    registry.register(DummyModule())  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        registry.register(DummyModule())  # type: ignore[arg-type]


def test_command_result_ok() -> None:
    assert CommandResult(0, "yes").ok
    assert not CommandResult(1, stderr="no").ok
