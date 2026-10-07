# Changelog

All notable changes are documented here.

## Unreleased

## 0.1.0 - 2026-09-25

### Added

- A declarative X1/Kali workstation profile with typed components for core tools, development, networking, wireless, security, and selected local applications.
- Read-only `doctor`, `inventory`, and `plan` commands plus a conservative, confirmed `apply` workflow with dry-run support.
- Narrow local providers for apt packages, uv tools, systemd services, dedicated Firefox profiles, and visible manual-only capabilities.
- An installable `field` command, version reporting, bundled runtime configuration templates, and user-local XDG-style configuration initialization.
- Profile validation, named user profile selection, packaging build checks, and a tag-triggered GitHub Release workflow.

### Safety

- Field-sidekick keeps planning inspectable and limits apply behavior to reviewed local actions. Account, vendor, device, secret, and remote-network workflows remain manual.

### Documentation

- Installation, configuration, CLI, contributor, security, and release guidance for the first public release.
