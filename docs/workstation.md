# Workstation notes

The target is a Kali Linux X1 field workstation, while the toolkit remains portable enough for development on another operating system. Linux-specific checks report `SKIP` or `WARN` on macOS rather than treating that development environment as broken.

Recommended workflow:

1. Install Python 3.13+ and uv.
2. Run `uv sync --all-groups`.
3. Review the desired state with `uv run field config show`.
4. Use `uv run field plan` (or `field plan dev` / `field plan wireless`) to compare it locally.
5. Review `uv run field apply --dry-run`; use `uv run field apply --yes` only for approved package/service changes.
6. Use `uv run field doctor` or `uv run field doctor wireless` to review local prerequisites.
7. Use `uv run field inventory` when documenting the machine.

The desired-state components deliberately separate reliable apt package names from intent that needs target-specific review. This iteration can install the listed apt packages and enable Docker's system service. It does not set up Python/uv, Docker Compose, eza, ProjectDiscovery httpx, PlatformIO/esptool, AI tools, Tailscale login, Syncthing pairing, Firefox profiles, Obsidian vaults, devices, network settings, scan networks, or contact remote services.
