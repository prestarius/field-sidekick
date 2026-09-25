from typer.testing import CliRunner

from field_sidekick import cli
from field_sidekick.cli import app
from field_sidekick.core import CheckResult, CheckStatus

runner = CliRunner()


def test_help_is_available() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "field" in result.output
    assert "doctor" in result.output


def test_inventory_is_available() -> None:
    result = runner.invoke(app, ["inventory"])
    assert result.exit_code == 0
    assert "inventory" in result.output


def test_modules_and_config_commands_are_available() -> None:
    assert runner.invoke(app, ["modules", "list"]).exit_code == 0
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "x1-kali-field" in result.output


def test_doctor_returns_nonzero_for_failed_check(monkeypatch) -> None:
    monkeypatch.setattr(
        cli,
        "collect_results",
        lambda registry, context, module: [
            CheckResult("dev", "Python", CheckStatus.FAIL, "too old")
        ],
    )
    result = runner.invoke(app, ["doctor", "dev"])
    assert result.exit_code == 1
    assert "FAIL" in result.output
