# 0002: Use explicit modules, checks, and desired-state profiles

## Status

Accepted.

## Decision

The application has a small core: `SidekickModule`, `Check`, `CheckResult`, `CheckStatus`, `CommandRunner`, `LocalPlatform`, and `ModuleRegistry`. Built-in modules are registered explicitly. YAML profiles describe the intended workstation, including modules that may not be implemented yet; they select implemented checks but are not applied in Iteration 2.

## Consequences

Checks have stable status semantics and are easy to test with fake command/platform data. The design avoids entry points, plugin discovery, and a generic task framework until there is a concrete need. A future desired-state apply operation requires a separate ADR and explicit user confirmation.
