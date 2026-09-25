# Architecture

`field-sidekick` uses a small application core and explicit built-in modules:

```text
CLI -> profile loader -> module registry -> system/dev/network/wireless checks
                                      |               |
                                      +-> common results +-> local platform/command boundary
```

The CLI owns user interaction. `Profile` validates desired state and selects enabled modules. `CheckResult` normalizes `PASS`, `WARN`, `FAIL`, and `SKIP`; the registry is an explicit list, not dynamic plugin discovery. `CommandRunner` and `LocalPlatform` are small seams for deterministic tests and portable behavior.

Iteration 2 checks only local state. A future apply workflow must have an explicit design, clear preview, confirmation, rollback considerations, and user opt-in. No module may introduce network scanning, exploitation, credential collection, persistence, or automatic network changes without a separate security decision.
