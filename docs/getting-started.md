# Getting started

## Prerequisites

Use Python 3.13 or newer and uv. The project currently applies state only on Kali/Debian Linux; it is still safe to inspect configuration and develop on macOS or another system.

When PyPI publishing is available:

```bash
uv tool install field-sidekick
```

Until then, install from the public repository:

```bash
uv tool install git+https://github.com/prestarius/field-sidekick.git
field --version
field config init
field config validate
```

## Inspect before changing

The bundled profile is the X1/Kali configuration. Start with read-only commands:

```bash
field config show
field doctor
field inventory
field plan
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
field apply --dry-run
field apply dev --dry-run
```

On a supported target, apply asks for confirmation unless `--yes` is supplied:

```bash
uv run field apply dev
```

Review the table first. `MANUAL` and `SKIP` entries cannot be applied. After applying, run `field plan` again to verify the resulting local state.

## Use your own profile

Run `field config init`, adapt the local profile and components, then pass it explicitly by path or name:

```bash
field config init
field plan --profile x1-kali
```

See [configuration](configuration.md) and the [X1/Kali walkthrough](examples/x1-kali-profile.md).
