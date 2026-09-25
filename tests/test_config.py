from pathlib import Path

import pytest

from field_sidekick.config import load_profile


def test_loads_x1_profile() -> None:
    profile = load_profile(Path("configs/profiles/x1-kali.yaml"))
    assert profile.name == "x1-kali-field"
    assert profile.modules["wireless"].settings["chipset"] == "MT7612U"
    assert {component.name for component in profile.components} >= {"core", "dev", "wireless"}
    assert any(package.name == "ripgrep" for package in profile.packages)


def test_rejects_invalid_profile(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("name: bad\nunexpected: value\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid profile"):
        load_profile(path)


def test_rejects_invalid_component(tmp_path: Path) -> None:
    component = tmp_path / "component.yaml"
    component.write_text("name: bad\nunexpected: value\n", encoding="utf-8")
    profile = tmp_path / "profile.yaml"
    profile.write_text("name: test\ninclude: [component.yaml]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid profile"):
        load_profile(profile)
