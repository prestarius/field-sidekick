# field-sidekick

`field-sidekick` is a declarative field-workstation management and security-engineering toolkit. Profiles express the intended X1/Kali workstation state; Iteration 2 uses that state to drive local readiness checks and does not apply it yet.

## Iteration 2 commands

```bash
uv run field --help
uv run field doctor
uv run field doctor wireless
uv run field inventory
uv run field modules list
uv run field config show
```

`doctor` aggregates `system`, `dev`, `network`, and `wireless` checks with `PASS`, `WARN`, `FAIL`, and `SKIP` outcomes. It checks local platform details, developer tools, Docker daemon access, interface/route/DNS configuration, and Linux wireless/USB metadata where available. macOS is supported as a development host and Linux-specific checks skip gracefully.

The default profile is [`configs/x1-kali.yaml`](configs/x1-kali.yaml). It also records desired state for later modules such as AI tooling, Tailscale, Syncthing, ESP32, Firefox, Obsidian, and OPSEC. Those declarations are deliberately not applied in this iteration.

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
