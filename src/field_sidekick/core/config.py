"""Desired-state profile configuration."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class ModuleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


class ProfileConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str
    target_os: str = "kali"
    modules: dict[str, ModuleConfig] = Field(default_factory=dict)

    def module(self, name: str) -> ModuleConfig:
        return self.modules.get(name, ModuleConfig(enabled=False))


def load_profile(path: Path) -> ProfileConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return ProfileConfig.model_validate(data)


def default_profile_path() -> Path:
    return Path("configs/profiles/x1-kali.yaml")
