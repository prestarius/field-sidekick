from typer.testing import CliRunner

from field_sidekick import cli
from field_sidekick.cli import app
from field_sidekick.core import CheckResult, CheckStatus
from field_sidekick.plan import PlanAction, PlanItem, PlanStatus

runner = CliRunner()


def test_help_is_available() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "field" in result.output
    assert "doctor" in result.output


def test_version_is_available() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_inventory_is_available() -> None:
    result = runner.invoke(app, ["inventory"])
    assert result.exit_code == 0
    assert "inventory" in result.output


def test_modules_and_config_commands_are_available() -> None:
    assert runner.invoke(app, ["modules", "list"]).exit_code == 0
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "x1-kali-field" in result.output


def test_config_path_and_validate_are_available(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = runner.invoke(app, ["config", "path"])
    validation = runner.invoke(app, ["config", "validate"])
    assert path.exit_code == 0
    assert "User config directory:" in path.output
    assert validation.exit_code == 0
    assert "Valid: x1-kali-field" in validation.output


def test_config_init_is_safe_by_default_and_force_replaces(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert runner.invoke(app, ["config", "init"]).exit_code == 0
    profile = tmp_path / "field-sidekick/profiles/x1-kali.yaml"
    profile.write_text("name: preserved\n", encoding="utf-8")
    assert runner.invoke(app, ["config", "init"]).exit_code == 0
    assert profile.read_text(encoding="utf-8") == "name: preserved\n"
    assert runner.invoke(app, ["config", "init", "--force"]).exit_code == 0
    assert "x1-kali-field" in profile.read_text(encoding="utf-8")


def test_config_validate_reports_invalid_explicit_profile(tmp_path) -> None:
    profile = tmp_path / "invalid.yaml"
    profile.write_text("name: invalid\nunexpected: true\n", encoding="utf-8")
    result = runner.invoke(app, ["config", "validate", "--profile", str(profile)])
    assert result.exit_code != 0
    assert "Invalid profile" in result.output


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


def test_plan_and_dry_run_are_read_only(monkeypatch) -> None:
    item = PlanItem(
        "dev", "apt", "package", "git", PlanStatus.MISSING, PlanAction.INSTALL_APT_PACKAGE, "git"
    )
    monkeypatch.setattr(cli, "build_plan", lambda context, scope: [item])
    applied: list[object] = []
    monkeypatch.setattr(cli, "apply_plan", lambda *args: applied.append(args))
    assert runner.invoke(app, ["plan", "dev"]).exit_code == 0
    result = runner.invoke(app, ["apply", "dev", "--dry-run"])
    assert result.exit_code == 0
    assert "no changes were made" in result.output
    assert not applied


def test_apply_requires_confirmation(monkeypatch) -> None:
    item = PlanItem(
        "dev", "apt", "package", "git", PlanStatus.MISSING, PlanAction.INSTALL_APT_PACKAGE, "git"
    )
    monkeypatch.setattr(cli, "build_plan", lambda context, scope: [item])
    monkeypatch.setattr(cli.typer, "confirm", lambda message: False)
    result = runner.invoke(app, ["apply", "dev"])
    assert result.exit_code == 1
    assert "Aborted" in result.output
