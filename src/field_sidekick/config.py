"""Typed, composable desired-state configuration for field workstations."""

import os
import shutil
import sys
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

PACKAGE_CONFIGS = files("field_sidekick").joinpath("data", "configs")
DEFAULT_PROFILE_NAME = "x1-kali"


class ModuleConfig(BaseModel):
    """Desired state for one module, including future modules."""

    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


class PackageSpec(BaseModel):
    """A package with a reliable package-manager mapping."""

    model_config = ConfigDict(extra="forbid")
    name: str
    apt: str | None = None

    @property
    def apt_name(self) -> str:
        return self.apt or self.name


class ServiceSpec(BaseModel):
    """A system service that may be enabled when systemd is available."""

    model_config = ConfigDict(extra="forbid")
    name: str
    enabled: bool = True
    scope: str = "system"
    managed: bool = True


class PythonToolSpec(BaseModel):
    """A Python CLI distributed as an installable uv tool."""

    model_config = ConfigDict(extra="forbid")
    name: str
    package: str | None = None

    @property
    def package_name(self) -> str:
        return self.package or self.name


class FirefoxProfileSpec(BaseModel):
    """A dedicated Firefox profile owned by this workstation profile."""

    model_config = ConfigDict(extra="forbid")
    name: str
    manage_privacy_preferences: bool = True


class ManualSpec(BaseModel):
    """A visible capability that is detected but deliberately never installed."""

    model_config = ConfigDict(extra="forbid")
    name: str
    command: str | None = None
    description: str = "user-managed"


class Component(BaseModel):
    """One focused slice of workstation desired state."""

    model_config = ConfigDict(extra="forbid")
    name: str
    description: str = ""
    packages: list[PackageSpec] = Field(default_factory=list)
    python_tools: list[PythonToolSpec] = Field(default_factory=list)
    services: list[ServiceSpec] = Field(default_factory=list)
    firefox_profiles: list[FirefoxProfileSpec] = Field(default_factory=list)
    manual: list[ManualSpec] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)


class Profile(BaseModel):
    """A portable, declarative workstation profile."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    name: str
    description: str = ""
    target: str = ""
    modules: dict[str, ModuleConfig] = Field(default_factory=dict)
    includes: list[str] = Field(default_factory=list, alias="include")
    components: list[Component] = Field(default_factory=list, exclude=True)

    @property
    def packages(self) -> list[PackageSpec]:
        """Return packages once, preserving the component order."""
        seen: set[str] = set()
        return [
            package
            for component in self.components
            for package in component.packages
            if not (package.apt_name in seen or seen.add(package.apt_name))
        ]


def user_config_dir() -> Path:
    """Return the per-user configuration directory without creating it."""
    if sys.platform == "darwin":
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / "Library/Application Support"))
    elif os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "field-sidekick"


def package_profile(name: str = DEFAULT_PROFILE_NAME):
    """Return a bundled, read-only profile resource by short name."""
    return PACKAGE_CONFIGS.joinpath("profiles", f"{name.removesuffix('.yaml')}.yaml")


def _profile_name(value: str) -> str:
    return value.removesuffix(".yaml")


def resolve_profile(value: str | Path | None = None) -> Path | Any:
    """Resolve an explicit path/name or the active user/bundled default profile.

    Explicit filesystem paths take precedence. Named profiles look in the user
    configuration directory first, then in the bundled templates. With no
    argument, a user ``profiles/x1-kali.yaml`` overrides the bundled default.
    """
    if value is not None:
        candidate = Path(value).expanduser()
        if candidate.is_file():
            return candidate
        name = _profile_name(str(value))
    else:
        name = DEFAULT_PROFILE_NAME

    user_profile = user_config_dir() / "profiles" / f"{name}.yaml"
    if user_profile.is_file():
        return user_profile
    bundled = package_profile(name)
    if bundled.is_file():
        return bundled
    raise ValueError(
        f"Profile {value!r} was not found. Use a path, add it under "
        f"{user_config_dir() / 'profiles'}, or run 'field config init'."
    )


def copy_bundled_configs(destination: Path, force: bool = False) -> list[Path]:
    """Copy packaged starter configs locally, refusing to replace files by default."""
    destination = destination.expanduser()
    copied: list[Path] = []
    for group in ("apps", "packages", "profiles"):
        for source in PACKAGE_CONFIGS.joinpath(group).iterdir():
            if not source.name.endswith(".yaml"):
                continue
            relative = Path(group) / source.name
            target = destination / relative
            if target.exists() and not force:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open("rb") as source_file, target.open("wb") as target_file:
                shutil.copyfileobj(source_file, target_file)
            copied.append(target)
    return copied


def load_profile(path: Path | Any) -> Profile:
    """Read a profile and its local component files without applying state."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Expected a mapping in {path}")
        profile = Profile.model_validate(data)
        components = []
        for relative_path in profile.includes:
            component_path = path.parent.joinpath(relative_path)
            component_data = yaml.safe_load(component_path.read_text(encoding="utf-8")) or {}
            if not isinstance(component_data, dict):
                raise ValueError(f"Expected a mapping in {component_path}")
            components.append(Component.model_validate(component_data))
        profile.components = components
        return profile
    except (OSError, ValidationError) as error:
        raise ValueError(f"Invalid profile {path}: {error}") from error
