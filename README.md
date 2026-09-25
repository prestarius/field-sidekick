# field-sidekick

`field-sidekick` is a declarative field-workstation management and security-engineering toolkit. The X1/Kali profile composes focused package and app components, then compares that intent with local state before any change is requested.

## Iteration 3 commands

```bash
uv run field --help
uv run field doctor
uv run field doctor wireless
uv run field inventory
uv run field modules list
uv run field config show
uv run field plan
uv run field plan packages
uv run field plan dev
uv run field plan wireless
uv run field apply --dry-run
uv run field apply packages --yes
```

`doctor` aggregates `system`, `dev`, `network`, and `wireless` checks with `PASS`, `WARN`, `FAIL`, and `SKIP` outcomes. It checks local platform details, developer tools, Docker daemon access, interface/route/DNS configuration, and Linux wireless/USB metadata where available. macOS is supported as a development host and Linux-specific checks skip gracefully.

The default profile is [`configs/profiles/x1-kali.yaml`](configs/profiles/x1-kali.yaml). It includes small component files for core, development, networking, wireless, security, ESP32, and apps. This makes it practical to review or plan a focused slice without copying a large package list into every profile.

`field plan` is always read-only and reports `OK`, `MISSING`, `CHANGE`, and `SKIP`. `field apply` acts only on missing apt packages and disabled systemd services, supports `--dry-run`, and prompts before changing anything unless `--yes` is supplied. Unsupported platforms—including macOS development machines—show `SKIP`; they do not attempt package or service operations. Browser, account-authenticated AI, Tailscale, Syncthing pairing, and device configuration remain declarative-only in this iteration.

## Development

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run pre-commit run --all-files
```

## Scope and safety

This project supports legitimate security-lab and workstation management. It is not an offensive automation framework: no scanning, exploitation, credential collection, persistence, lateral movement, or automatic network changes are included. See [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), and [project scope](docs/decisions/0001-project-scope.md).

## License

MIT. See [LICENSE](LICENSE).
