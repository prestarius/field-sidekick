from pathlib import Path

from typer.testing import CliRunner

from field_sidekick.cli import app

runner = CliRunner()


def profile(tmp_path: Path) -> Path:
    path = tmp_path / "profile.yaml"
    path.write_text(
        "profile: test\n"
        "target_os: kali\n"
        "modules:\n"
        "  system:\n"
        "    enabled: true\n"
        "  dev:\n"
        "    enabled: true\n"
        "  network:\n"
        "    enabled: true\n"
        "  wireless:\n"
        "    enabled: true\n",
        encoding="utf-8",
    )
    return path


def test_help_lists_main_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

    for command in ("doctor", "inventory", "modules", "config"):
        assert command in result.output


def test_modules_list(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["modules", "list", "--profile", str(profile(tmp_path))],
    )
    assert result.exit_code == 0
    assert "system" in result.output
    assert "wireless" in result.output


def test_config_show(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["config", "show", "--profile", str(profile(tmp_path))],
    )
    assert result.exit_code == 0
    assert "target_os" in result.output


def test_unknown_doctor_module_is_rejected(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["doctor", "wat", "--profile", str(profile(tmp_path))],
    )
    assert result.exit_code != 0
