from pathlib import Path

from field_sidekick.config import load_profile


def test_loads_x1_profile() -> None:
    config = load_profile(Path("configs/profiles/x1-kali.yaml"))
    assert config.profile == "x1-kali"
    assert config.target_os == "kali"
    assert config.module("wireless").settings["chipset"] == "MT7612U"
