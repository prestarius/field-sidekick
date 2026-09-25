from pathlib import Path

import pytest

from field_sidekick.config import load_profile


def test_loads_x1_profile() -> None:
    profile = load_profile(Path("configs/x1-kali.yaml"))
    assert profile.name == "x1-kali-field"
    assert profile.modules["wireless"].settings["chipset"] == "MT7612U"


def test_rejects_invalid_profile(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("name: bad\nunexpected: value\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid profile"):
        load_profile(path)
