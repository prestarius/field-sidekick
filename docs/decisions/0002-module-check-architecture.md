# 0002: Module and check architecture

## Status

Accepted.

## Context

The first scaffold placed most doctor behavior in one module and represented availability as booleans. That model does not scale to richer workstation domains.

## Decision

Use a small module boundary:

- `SidekickModule` owns checks for one domain.
- `Check` is an executable local probe.
- `CheckResult` carries a typed status and detail.
- `CommandRunner` owns subprocess execution.
- `ModuleRegistry` owns module selection.
- `ProfileConfig` describes desired state.

Status semantics:

- PASS — desired capability is healthy.
- WARN — usable but incomplete, optional capability missing, or target mismatch.
- FAIL — required capability is not healthy.
- SKIP — the check cannot or should not run in the current environment.

## Consequences

Tests can replace runner/platform dependencies without depending on the host machine. Future install/apply operations can reuse the same module boundaries without turning the CLI into a collection of shell commands.
