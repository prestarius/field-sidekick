# Architecture

`field-sidekick` uses a small application core and explicit built-in modules:

```text
CLI -> composed profile loader -> module registry -> system/dev/network/wireless checks
              |                         |               |
              +-> plan builder ---------+               +-> local platform/command boundary
                         |
                         +-> apt package / systemd service adapters -> explicit apply
```

The CLI owns user interaction. A `Profile` validates its `include` list and each typed component; package and service records therefore have one clear source of truth. `CheckResult` normalizes readiness checks, while `PlanItem` normalizes desired-state differences as `OK`, `MISSING`, `CHANGE`, and `SKIP`. The registry is an explicit list, not dynamic plugin discovery. `CommandRunner` and `LocalPlatform` are small seams for deterministic tests and portable behavior.

Iteration 3 keeps planning read-only. Application is deliberately narrow: the apt adapter can install a reliably named missing package and the systemd adapter can enable/start a declared service. Each operation is idempotent because planning detects the already-installed or enabled state first. Apply requires `--yes` or an interactive confirmation; `--dry-run` never executes a command. Non-Linux/non-systemd environments skip safely. No module may introduce network scanning, exploitation, credential collection, persistence, or automatic network changes without a separate security decision.
