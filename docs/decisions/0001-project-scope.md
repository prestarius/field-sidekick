# 0001: Keep v0.1 local, safe, and non-offensive

## Status

Accepted.

## Context

The project supports a security-focused field workstation. That context can invite automation with unexpectedly broad consequences.

## Decision

At the time of this decision, v0.1 provided only read-only local health checks and inventory. Configuration files were declarative examples and were never applied. The project does not automate reconnaissance, exploitation, password attacks, persistence, lateral movement, or network changes.

## Consequences

The initial release is useful for repeatable workstation visibility while retaining a conservative security posture. Subsequent provider-backed local apply behavior is recorded in later decisions and retains explicit scope, documentation, test coverage, and an opt-in interaction model.
