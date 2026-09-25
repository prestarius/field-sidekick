# 0001: Project scope

## Status

Accepted.

## Decision

field-sidekick is a **declarative field-workstation management and security-engineering toolkit**.

Its intended scope includes repeatable workstation setup, local health checks, developer and AI tooling, networking, wireless adapters, ESP32 devices, browser compartmentalization, synchronization and authorized security-lab workflows.

The project is not limited to read-only visibility. Future versions may perform explicit system changes through idempotent, reviewable install/apply operations.

The project does not aim to become an autonomous exploitation, credential-theft, persistence or covert-access framework. Security functionality should be designed around owned or explicitly authorized environments.

## Consequences

The architecture must support both inspection and future desired-state application without coupling the CLI directly to system commands.
