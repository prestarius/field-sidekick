# field-sidekick

`field-sidekick` is a declarative field-workstation management and security-engineering toolkit. Its primary target is a Kali Linux ThinkPad used as a portable sidekick for engineering, authorized security research, wireless work, ESP32 experimentation, AI tooling and homelab operations.

The project follows a simple model: **desired state + local inspection + explicit actions**. Iteration 2 implements the desired-state profile and local doctor architecture. Mutating commands such as install/apply come later and will be explicit, reviewable and idempotent.

## Commands

```bash
uv run field --help
uv run field doctor
uv run field doctor system
uv run field doctor dev
uv run field doctor network
uv run field doctor wireless
uv run field inventory
uv run field modules list
uv run field config show
```

The default profile is `configs/profiles/x1-kali.yaml`.

## Architecture

Built-in modules implement a small `SidekickModule` contract and expose typed checks. Doctor aggregates `PASS`, `WARN`, `FAIL` and `SKIP` results. The CLI consumes a validated Pydantic desired-state profile rather than disconnected YAML placeholders.

Iteration 2 intentionally keeps checks local and non-destructive while establishing the architecture required for future `field install` / `field apply` workflows.

## Scope

This is a security-engineering workstation toolkit, not a generic inventory toy and not an autonomous offensive framework. Legitimate workstation management, lab setup, adapter/firmware visibility, developer tooling and authorized security workflows are in scope. Destructive or covert automation is not part of the current design.

## Development

Requires Python 3.13+ and uv.

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## License

MIT. See [LICENSE](LICENSE).
