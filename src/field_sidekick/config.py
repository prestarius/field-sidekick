"""Typed, composable desired-state configuration for field workstations."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


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


DEFAULT_PROFILE_PATH = Path("configs/profiles/x1-kali.yaml")


def load_profile(path: Path) -> Profile:
    """Read a profile and its local component files without applying state."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    try:
        profile = Profile.model_validate(data)
        components = []
        for relative_path in profile.includes:
            component_path = path.parent / relative_path
            component_data = yaml.safe_load(component_path.read_text(encoding="utf-8")) or {}
            if not isinstance(component_data, dict):
                raise ValueError(f"Expected a mapping in {component_path}")
            components.append(Component.model_validate(component_data))
        profile.components = components
        return profile
    except ValidationError as error:
        raise ValueError(f"Invalid profile {path}: {error}") from error
