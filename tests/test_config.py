from pathlib import Path

import pytest

from field_sidekick.config import (
    copy_bundled_configs,
    load_profile,
    package_profile,
    resolve_profile,
    user_config_dir,
)


def test_loads_x1_profile() -> None:
    profile = load_profile(package_profile())
    assert profile.name == "x1-kali-field"
    assert profile.modules["wireless"].settings["chipset"] == "MT7612U"

    component_names = {component.name for component in profile.components}
    assert component_names >= {
        "core",
        "dev",
        "wireless",
        "opsec",
        "wormhole",
        "editors",
    }

    package_names = {package.name for package in profile.packages}
    assert {"ripgrep", "lsof", "strace", "rsync", "masscan", "blueman"} <= package_names


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


def test_user_config_dir_uses_xdg_location(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert user_config_dir() == tmp_path / "field-sidekick"


def test_config_init_never_overwrites_without_force(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    destination = user_config_dir()
    copied = copy_bundled_configs(destination)
    profile_path = destination / "profiles/x1-kali.yaml"
    profile_path.write_text("name: preserved\n", encoding="utf-8")

    assert copied
    assert copy_bundled_configs(destination) == []
    assert profile_path.read_text(encoding="utf-8") == "name: preserved\n"

    copy_bundled_configs(destination, force=True)
    assert "x1-kali-field" in profile_path.read_text(encoding="utf-8")


def test_named_user_profile_overrides_bundled_profile(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    destination = user_config_dir()
    copy_bundled_configs(destination)
    selected = resolve_profile("x1-kali")
    assert selected == destination / "profiles/x1-kali.yaml"


def test_bundled_resource_loads_outside_repository(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    profile = load_profile(resolve_profile())
    assert profile.name == "x1-kali-field"
