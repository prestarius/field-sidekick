# Configuration

## Composition model

A profile is a YAML mapping with metadata, optional diagnostic module settings, and an `include` list. Each included file is a component. Include paths are resolved relative to the profile file, not the repository root.

```yaml
name: my-workstation
description: My local workstation intent.
target: Kali Linux
include:
  - ../packages/core.yaml
  - ../apps/firefox.yaml
modules:
  system: {enabled: true, settings: {distribution: kali}}
```

The loader keeps component order. It validates profiles and components with strict schemas, so misspelled or unsupported fields fail rather than being silently ignored.

## Component fields

Each component needs `name`; `description` is optional. A component may contain these typed lists:

| Field | Record fields | Meaning |
| --- | --- | --- |
| `packages` | `name`, optional `apt` | Package name and optional apt mapping |
| `python_tools` | `name`, optional `package` | CLI package installed by `uv tool` |
| `services` | `name`, optional `enabled`, `scope`, `managed` | systemd service intent; scope is `system` or `user` |
| `firefox_profiles` | `name`, optional `manage_privacy_preferences` | Dedicated Firefox profile intent |
| `manual` | `name`, optional `command`, `description` | Visible, detection-only capability |
| `capabilities` | strings | Declarative user-managed intent |

`managed: false` keeps a service visible as `MANUAL`; it does not enable or start it. `enabled: false` represents a service that should not be enabled, but does not stop an already running service.

## Example component

Create a focused component under `configs/apps/` or `configs/packages/` and include it from a profile:

```yaml
name: my-tools
description: Locally reviewed command-line tools.
packages:
  - {name: jq}
python_tools:
  - {name: platformio}
manual:
  - {name: Example account, command: example, description: login remains manual}
```

Use `field config show --profile PATH` to inspect the fully loaded result, then `field plan --profile PATH` to review it. Do not add credentials, tokens, private paths, or machine-specific secrets to tracked configuration.

The bundled X1 profile and its components are the most complete working reference: [`configs/profiles/x1-kali.yaml`](../configs/profiles/x1-kali.yaml).
