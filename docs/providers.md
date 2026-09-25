# Providers

Providers are explicit built-in local-state adapters. They are selected by component field, not configured dynamically.

| Provider | Source field | Supported when | Action |
| --- | --- | --- | --- |
| `apt` | `packages` | Linux with `dpkg-query` | `sudo apt-get install --yes PACKAGE` |
| `uv-tool` | `python_tools` | Linux with `uv` | `uv tool install PACKAGE` |
| `systemd` | `services` with system scope | Linux with `systemctl` | `sudo systemctl enable --now SERVICE` |
| `systemd-user` | `services` with user scope | Linux with `systemctl` | `systemctl --user enable --now SERVICE` |
| `firefox` | `firefox_profiles` | Linux | Creates named dedicated profile; updates marked `user.js` block |
| `manual` | `manual`, `capabilities`, unmanaged services | Always visible | Detection only, no action |

Provider support is evaluated when building the plan. If a provider is unavailable, its entry is `SKIP`; it is never attempted. An apt package or `uv tool` entry can be `MISSING`, a service can be `CHANGE`, and a Firefox profile/config can be `MISSING` or `CHANGE`. Already matching state is `OK`.

Firefox does not select or modify the default profile. It only addresses names declared in the selected profile. The managed preferences are constrained to a marked block and disable password saving plus address/payment autofill.

The manual provider is deliberately not a fallback installer. Vendor repositories, accounts, login, network enrollment, device pairing, secrets, and ambiguous package mappings remain manual.
