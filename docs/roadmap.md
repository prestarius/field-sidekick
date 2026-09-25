# Roadmap

## Iteration 2 — declarative checks (complete)

- Desired-state X1/Kali profile and explicit module registry.
- Local `system`, `dev`, `network`, and `wireless` checks.
- No desired-state application or offensive automation.

## Iteration 3 — composed desired state and safe apply foundation (complete)

- Composable, validated profile components for packages and application intent.
- Read-only `plan` for full or scoped desired-state comparison.
- Explicit, dry-run capable, confirmed apt package and systemd service actions only.
- Apps, user authentication, device setup, and uncertain package mappings remain declarative-only.

## Iteration 4 — providers and local workstation bootstrap (complete)

- Explicit apt, uv-tool, systemd, systemd-user, Firefox, and manual providers.
- Actionable Docker package/service, Syncthing package/user service, PlatformIO and esptool tools.
- Dedicated `ai`, `research`, and `burner` Firefox profiles with scoped local autofill/password-saving preferences.
- Manual detection for Tailscale; vendor setup and login are never automated.

## Later candidates

- Documented, opt-in profiles for workstation applications.
- Exportable local reports and hardware inventory.
- Additional modules only after a scoped design decision and safety review.
