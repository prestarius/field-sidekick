# Architecture

`field-sidekick` uses a small application core and explicit built-in modules:

```text
CLI -> composed profile loader -> module registry -> system/dev/network/wireless checks
              |                         |               |
              +-> plan builder ---------+               +-> local platform/command boundary
                         |
                         +-> apt / uv-tool / systemd / Firefox providers -> explicit apply
```

The CLI owns user interaction. A `Profile` validates its `include` list and each typed component; package and service records therefore have one clear source of truth. `CheckResult` normalizes readiness checks, while `PlanItem` normalizes desired-state differences as `OK`, `MISSING`, `CHANGE`, and `SKIP`. The registry is an explicit list, not dynamic plugin discovery. `CommandRunner` and `LocalPlatform` are small seams for deterministic tests and portable behavior.

Iteration 4 retains a deliberately small provider layer, not dynamic plugin discovery. Apt owns Kali/Debian packages; `uv tool` owns Python CLIs with a real entry point; systemd and systemd-user own enabled/running service state; Firefox owns only the named dedicated profiles and a marked block in their `user.js`; the manual provider detects but never installs vendor/account-bound capabilities. Planning is read-only and distinguishes `OK`, `MISSING`, `CHANGE`, `SKIP`, and `MANUAL`. Apply requires `--yes` or an interactive confirmation; `--dry-run` never executes a command. No provider logs in, changes credentials, enrolls a remote network, pairs Syncthing, or changes an unrelated Firefox profile.
