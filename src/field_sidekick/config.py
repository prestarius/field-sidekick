"""Configuration loading for future, opt-in workstation modules."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class WorkspaceConfig(BaseModel):
    """Minimal common schema for declarative module configuration."""

    model_config = ConfigDict(extra="allow")

    name: str
    enabled: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


def load_config(path: Path) -> WorkspaceConfig:
    """Load one YAML configuration file without applying its settings."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return WorkspaceConfig.model_validate(data)
