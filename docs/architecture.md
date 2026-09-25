# Architecture

Field-sidekick has a small application core and explicit built-in boundaries:

```text
CLI -> profile loader -> typed profile + components -> plan builder -> providers -> local system
 |             |                 |                       |
 |             +-> YAML          +-> module registry      +-> rendered plan / confirmed apply
 +-> doctor, inventory
```

The CLI owns command parsing, rendering, and confirmation. `load_profile()` reads a top-level profile and the component files named by its `include` list; Pydantic validates both layers and rejects unknown fields. Component order is preserved, making the plan stable and reviewable.

The diagnostic side is separate from desired-state application. The explicit module registry contains `system`, `dev`, `network`, and `wireless` checks. `CommandRunner` and `LocalPlatform` provide narrow seams for deterministic tests and graceful behavior off the Linux target.

The planner converts component records into `PlanItem` values with `OK`, `MISSING`, `CHANGE`, `SKIP`, or `MANUAL` status. Planning is always read-only. Application receives only plan items with a non-`NONE` action and is gated by an interactive confirmation or `--yes`.

Providers are intentionally concrete rather than dynamically discovered: apt, `uv tool`, systemd, systemd-user, Firefox, and manual detection. This is not a plugin framework. Adding a provider means adding a small, testable built-in capability with a clear platform check and safety boundary; see [development](development.md).

Firefox handles only explicitly named profiles and a marked block in their `user.js`. The manual provider exposes intent or local detection but never installs vendor software, logs in, enrolls a service, pairs devices, or changes remote state.

Related decisions are recorded in [`docs/decisions/`](decisions/).
