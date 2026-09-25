# Roadmap

The roadmap describes intended direction, not release commitments. Each expansion should preserve explicit review, local-only scope, and safety boundaries.

## Iteration 2 — Declarative checks (complete)

- Added the desired-state X1/Kali profile and explicit module registry.
- Added local `system`, `dev`, `network`, and `wireless` checks.

## Iteration 3 — Composed desired state and safe apply foundation (complete)

- Added composable, validated profile components and read-only planning.
- Added confirmed, dry-run-capable apt package and systemd service actions.

## Iteration 4 — Providers and local workstation bootstrap (complete)

- Added explicit apt, uv-tool, systemd, systemd-user, Firefox, and manual providers.
- Added actionable Docker, Syncthing, PlatformIO, esptool, and scoped Firefox profile support.

## Iteration 5 — Documentation & public readiness (complete)

- Rebuilt user and contributor documentation around the current CLI and configuration model.
- Added community files, issue templates, and a public-readiness review.

## Iteration 6 — Installation / packaging / first public release

- Define supported installation paths and release/versioning process.
- Validate package metadata and publish only after release checks are repeatable.

## Iteration 7 — Workstation app providers

- Evaluate additional narrowly scoped, opt-in local app providers.
- Keep vendor repositories, accounts, and remote enrollment manual unless separately designed and reviewed.

## Iteration 8 — Hardware & field diagnostics

- Expand read-only hardware, adapter, and field-readiness diagnostics.
- Prefer exportable local reports over automatic remediation.

## Iteration 9 — Profiles / overlays / reproducibility

- Design profile overlays and reproducible profile selection without obscuring final intent.
- Add validation and documentation before introducing composition beyond the current include model.
