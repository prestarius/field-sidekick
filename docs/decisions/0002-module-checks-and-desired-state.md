# 0002: Use explicit modules, checks, and desired-state profiles

## Status

Accepted.

## Decision

The application has a small core: `SidekickModule`, `Check`, `CheckResult`, `CheckStatus`, `CommandRunner`, `LocalPlatform`, and `ModuleRegistry`. Built-in modules are registered explicitly. At the time of this decision, YAML profiles selected implemented checks but were not applied; later decisions add the current provider-backed desired-state behavior.

## Consequences

Checks have stable status semantics and are easy to test with fake command/platform data. The design avoids entry points, plugin discovery, and a generic task framework until there is a concrete need. Desired-state apply was subsequently added through separate decisions with explicit user confirmation.
