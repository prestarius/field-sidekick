from pathlib import Path

from field_sidekick.config import load_config


def test_loads_kali_config() -> None:
    config = load_config(Path("configs/kali.yaml"))
    assert config.name == "kali"
    assert config.enabled is True
    assert config.settings["update_policy"] == "manual"
