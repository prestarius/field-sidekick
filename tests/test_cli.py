from typer.testing import CliRunner

from field_sidekick.cli import app

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
