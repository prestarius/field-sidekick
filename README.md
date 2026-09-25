# field-sidekick

`field-sidekick` is a small, safe-by-default companion for maintaining a Kali Linux field workstation. It provides a concise local health check and inventory without configuring systems, scanning networks, or automating offensive activity.

## v0.1 commands

```bash
uv run field --help
uv run field doctor
uv run field inventory
```

`doctor` checks local OS and tool availability only. `inventory` reports a compact machine and development-tool summary. Neither command changes the workstation or communicates with external services.

## Development

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run pre-commit run --all-files
```

## Scope and safety

This project is a workstation-management foundation, not a penetration-testing automation framework. Its modular layout leaves room for documented, opt-in integrations while keeping v0.1 deliberately local and non-offensive. See [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), and [project scope](docs/decisions/0001-project-scope.md).

## License

MIT. See [LICENSE](LICENSE).
