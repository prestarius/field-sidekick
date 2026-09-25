# 0004: Keep providers explicit and Firefox changes profile-scoped

## Status

Accepted.

## Decision

Iteration 4 uses a fixed set of small providers rather than a plugin framework. The planner owns provider selection; the CLI only renders and confirms a plan. Apt, `uv tool`, systemd, systemd-user, Firefox, and manual detection have narrow interfaces and are all exercised with fake runner/platform state in tests.

Firefox management creates only explicitly declared named profiles. It does not invoke Firefox, replace a profile directory, or touch default and personal profiles. Managed privacy settings are written as a delimited block in `user.js`, preserving unrelated lines. Tailscale, account login, credentials, remote enrollment, and vendor repository bootstrapping remain manual.

## Consequences

The X1 bootstrap becomes useful for reliable local state without becoming a distribution manager or identity-management tool. `bleak` stays declarative because it is a library with no stable standalone `uv tool` semantics; esptool and PlatformIO are actionable CLIs.
