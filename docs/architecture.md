# Architecture

`field-sidekick` uses a small application core and a future-facing module boundary:

```text
CLI -> read-only services (doctor, inventory) -> local OS/tool metadata
                 |
                 +-> config loader -> YAML declarations
                 +-> modules/ (future, opt-in integrations)
```

The CLI owns user interaction. `doctor` and `inventory` collect only local information. `config` validates declarative YAML but does not apply it. `modules` is intentionally empty in v0.1 so integrations can be added with isolated permissions, documented behavior, and tests.

No module may introduce network scanning, exploitation, credential collection, persistence, or automatic system changes without an explicit future design decision and user opt-in.
