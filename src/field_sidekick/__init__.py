"""Safe local workstation checks for field-sidekick."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("field-sidekick")
except PackageNotFoundError:  # pragma: no cover - direct source-tree import only
    __version__ = "0+unknown"
