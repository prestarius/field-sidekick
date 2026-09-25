# field-sidekick

`field-sidekick` is a declarative field-workstation management and security-engineering toolkit. The X1/Kali profile composes focused package and app components, then compares that intent with local state before any change is requested.

## Iteration 4 commands

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

`field plan` is always read-only and reports `OK`, `MISSING`, `CHANGE`, `SKIP`, and `MANUAL`, with an explicit provider column. `field apply` supports apt packages, `uv tool` CLI packages, system and user systemd services, and dedicated Firefox profile configuration. It supports `--dry-run` and prompts before changing anything unless `--yes` is supplied.

Example excerpt:

```text
Scope      Provider      Kind          Name                Status   Action
dev        apt           package       docker.io           MISSING  INSTALL_APT_PACKAGE
dev        systemd       service       docker.service      CHANGE   ENABLE_SYSTEM_SERVICE
esp32      uv-tool       python-tool   esptool             MISSING  INSTALL_PYTHON_TOOL
syncthing  systemd-user  service       syncthing.service   CHANGE   ENABLE_USER_SERVICE
firefox    firefox       profile       research            MISSING  CREATE_FIREFOX_PROFILE
firefox    firefox       config        research privacy    CHANGE   CONFIGURE_FIREFOX_PREFERENCES
tailscale  manual        service       tailscaled.service  MANUAL   NONE
```

`field apply --dry-run` renders this same plan and makes no changes. Unsupported platforms—including macOS development machines—show `SKIP`; they do not attempt package, service, or Firefox operations. Tailscale vendor-repository setup/login, Syncthing pairing, AI tools, editors, VPNs, secrets, and other account-bound tools remain `MANUAL`.

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
