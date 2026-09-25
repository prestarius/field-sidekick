# Getting started

## Prerequisites

Use Python 3.13 or newer and uv. The project currently applies state only on Kali/Debian Linux; it is still safe to inspect configuration and develop on macOS or another system.

```bash
git clone https://github.com/prestarius/field-sidekick.git
cd field-sidekick
uv sync --all-groups
```

## Inspect before changing

The bundled profile is the X1/Kali configuration. Start with read-only commands:

```bash
uv run field config show
uv run field doctor
uv run field inventory
uv run field plan
```

`doctor` performs local readiness checks. `inventory` prints a concise machine/tool summary. `plan` compares the profile with local state and reports `OK`, `MISSING`, `CHANGE`, `SKIP`, and `MANUAL` rows.

Narrow a plan to one component when reviewing it:

```bash
uv run field plan dev
uv run field plan firefox
uv run field plan packages
```

The `packages` scope includes package entries across all components. Other scopes must match a component name in the selected profile.

## Dry run and apply

`field apply --dry-run` renders the same plan and performs no action:

```bash
uv run field apply --dry-run
uv run field apply dev --dry-run
```

On a supported target, apply asks for confirmation unless `--yes` is supplied:

```bash
uv run field apply dev
```

Review the table first. `MANUAL` and `SKIP` entries cannot be applied. After applying, run `field plan` again to verify the resulting local state.

## Use your own profile

Copy the minimal profile into `configs/profiles/`, adapt its component includes, then pass it explicitly:

```bash
cp docs/examples/minimal-profile.yaml configs/profiles/my-workstation.yaml
uv run field plan --profile configs/profiles/my-workstation.yaml
```

See [configuration](configuration.md) and the [X1/Kali walkthrough](examples/x1-kali-profile.md).
