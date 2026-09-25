# field-sidekick

`field-sidekick` is a small declarative toolkit for checking and bootstrapping a security-engineering workstation. A profile describes intended local state; `field` compares that intent with the machine, shows a plan, and can apply only a narrow set of reviewed local actions.

It exists to make a workstation repeatable without turning it into an opaque installer. The project favors explicit YAML, read-only previews, small built-in providers, and visible manual boundaries over broad automation.

It is for people maintaining their own Kali/Debian-based field or lab workstation and who want configuration they can inspect, version, and adapt. It is not a fleet manager, a general-purpose provisioning system, or an offensive-security automation framework.

The current actionable target is Kali/Debian Linux. macOS and other systems are useful development hosts: local checks may run, while Linux-specific plan entries report `SKIP` and are not applied. See [workstation notes](docs/workstation.md).

## Quick start

Requirements: Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/prestarius/field-sidekick.git
cd field-sidekick
uv sync --all-groups

# Inspect the bundled profile and compare it with this machine.
uv run field config show
uv run field plan

# Render exactly what an apply would consider, without changing anything.
uv run field apply --dry-run
```

On a Kali/Debian target, review the plan before applying it. `apply` prompts by default; `--yes` is an explicit non-interactive confirmation.

```bash
uv run field apply dev
uv run field apply dev --yes
```

Do not use `--yes` until you have reviewed the selected scope and understand each action. [Getting started](docs/getting-started.md) explains the workflow in detail.

## Concepts

- **Profile**: a top-level YAML file describing a workstation and listing component files to include.
- **Component**: one focused, typed slice of desired state, such as `dev`, `wireless`, or `firefox`.
- **Provider**: a small built-in implementation that inspects or applies one kind of local state.
- **Plan**: the read-only comparison between configured intent and the local machine. `field plan` never makes changes.
- **Apply**: the confirmed execution of actionable plan entries. `field apply --dry-run` also never makes changes.
- **Actionable vs. MANUAL**: an actionable entry has a reviewed local action. `MANUAL` remains visible and may be detected, but field-sidekick will never install, log in, pair, enroll, or otherwise configure it.

## Configuration

The bundled profile is [`configs/profiles/x1-kali.yaml`](configs/profiles/x1-kali.yaml). Its `include` list composes focused YAML components from:

- [`configs/packages/`](configs/packages/) for apt package groups;
- [`configs/apps/`](configs/apps/) for app, service, Firefox, and manual intent;
- [`configs/profiles/`](configs/profiles/) for top-level profiles.

Create a profile by copying the minimal example, point its `include` paths at your components, then use it with `--profile`:

```bash
cp docs/examples/minimal-profile.yaml configs/profiles/my-workstation.yaml
uv run field plan --profile configs/profiles/my-workstation.yaml
uv run field apply --profile configs/profiles/my-workstation.yaml --dry-run
```

Component paths are resolved relative to the profile file. All profile and component fields are validated; unknown fields are rejected. Read [configuration](docs/configuration.md) before changing a profile.

## Providers and current coverage

| Provider | Current support | Apply behavior |
| --- | --- | --- |
| `apt` | Kali/Debian packages | Installs a listed package with `sudo apt-get install --yes` |
| `uv-tool` | Python CLI tools | Runs `uv tool install` for listed CLI packages |
| `systemd` | System services | Enables and starts a service with `sudo` |
| `systemd-user` | Per-user services | Enables and starts a user service without `sudo` |
| `firefox` | Named Linux Firefox profiles | Creates dedicated profiles and manages a marked `user.js` block |
| `manual` | Account/vendor/device-bound capabilities | Detects only; never applies |

Details, platform conditions, and boundaries are in [providers](docs/providers.md).

## CLI overview

```bash
uv run field --help
uv run field doctor [system|dev|network|wireless]
uv run field inventory
uv run field modules list
uv run field config show [--profile PATH]
uv run field plan [SCOPE] [--profile PATH]
uv run field apply [SCOPE] [--dry-run] [--yes] [--profile PATH]
```

`SCOPE` is a component name from the selected profile (for example `dev`, `wireless`, or `firefox`). `packages` is also accepted as an alias for package entries across all components. See the [CLI reference](docs/cli.md).

## Safety and non-goals

Field-sidekick is local, explicit, and conservative. It does not automate scanning, exploitation, credential collection, password attacks, persistence, lateral movement, remote network changes, account login, device pairing, or secret handling. It does not modify an existing Firefox profile; it only manages explicitly named dedicated profiles it creates or finds by name. See [safety](docs/safety.md).

## Development and contributing

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Read [development](docs/development.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before opening a change.

## Status and roadmap

The project has a working profile loader, local diagnostics, read-only planning, and a deliberately narrow set of provider-backed actions. Packaging, broader workstation providers, hardware diagnostics, and profile overlays are planned next. See the [roadmap](docs/roadmap.md) and [architecture](docs/architecture.md).

## License

MIT. See [LICENSE](LICENSE).
