# 0003: Compose desired state and constrain apply

## Status

Accepted.

## Decision

Profiles contain workstation identity, enabled check modules, and a local `include` list. Each included YAML component has typed packages, services, and declarative capabilities. Package and service operations are behind small apt and systemd interfaces. Planning only reads local state; applying requires a confirmation or `--yes`, and supports `--dry-run`.

## Consequences

Package names are recorded only where the Kali/Debian mapping is sufficiently clear. Everything that depends on a vendor repository, authentication, a user service, hardware, or an uncertain mapping remains a visible declarative capability. This preserves reviewability and avoids turning the project into a distro wrapper. The narrow adapters make a future macOS/Homebrew implementation possible without putting package-manager logic in the CLI.
