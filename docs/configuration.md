# Configuration

## Installed configuration

Installed users do not edit the package or a cloned repository. The packaged X1/Kali YAML is a read-only template. Initialize a local copy once:

```bash
field config init
field config path
field config validate
```

On Linux, the default directory is `~/.config/field-sidekick`; `XDG_CONFIG_HOME` is respected. macOS uses `~/Library/Application Support/field-sidekick` unless `XDG_CONFIG_HOME` is set, and Windows uses `%APPDATA%\\field-sidekick`.

`config init` copies `apps/`, `packages/`, and `profiles/` from the package. It never overwrites an existing YAML file. Use `field config init --force` only when you intentionally want to restore the shipped starter files. This is local file copying only; it never applies workstation state.

`--profile /absolute/or/relative/path.yaml` selects that exact file. `--profile name` resolves `profiles/name.yaml` from user configuration first and then from bundled templates. With no option, `x1-kali` follows the same precedence. Component paths remain relative to their profile file.

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

Create a focused component under your user configuration `apps/` or `packages/` directory and include it from a profile:

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

Use `field config validate --profile PATH_OR_NAME` before `field config show` or `field plan`. Do not add credentials, tokens, private paths, or machine-specific secrets to tracked configuration.

The bundled X1 profile and its components are the most complete working reference: [`configs/profiles/x1-kali.yaml`](../configs/profiles/x1-kali.yaml).
