# Development

## Setup

Use Python 3.13+ and uv:

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Run the CLI through uv while developing:

```bash
uv run field --help
uv run field plan
uv run field apply --dry-run
```

`plan` is always read-only. `--dry-run` belongs to `apply` and renders that command's plan without changing the machine.

## Design boundaries

Keep application behavior explicit and narrow. The core owns YAML validation, planning, and CLI confirmation; providers own their local state checks and actions. Do not introduce dynamic provider discovery or a plugin framework for a single provider.

When changing a profile schema, update the Pydantic models, tests, configuration documentation, examples, and the relevant built-in YAML together. Unknown fields must remain rejected.

When adding a provider, implement a small concrete class with: a clear support predicate, read-only state inspection, a bounded local action, plan rendering, tests using fake runner/platform state, and a documented safety boundary. Account, vendor, remote, and secret-dependent workflows should remain `MANUAL` unless separately designed and reviewed.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution workflow.
