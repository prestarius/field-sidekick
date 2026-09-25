"""Desired-state profile loading for field workstations.

Profiles describe intent only in Iteration 2; they are never applied.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ModuleConfig(BaseModel):
    """Desired state for one module, including future modules."""

    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


class Profile(BaseModel):
    """A portable, declarative workstation profile."""

    model_config = ConfigDict(extra="forbid")
    name: str
    description: str = ""
    target: str = ""
    modules: dict[str, ModuleConfig] = Field(default_factory=dict)


DEFAULT_PROFILE_PATH = Path("configs/x1-kali.yaml")


def load_profile(path: Path) -> Profile:
    """Read and validate a profile without applying desired state."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    try:
        return Profile.model_validate(data)
    except ValidationError as error:
        raise ValueError(f"Invalid profile {path}: {error}") from error
