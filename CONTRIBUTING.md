# Contributing

Thanks for helping improve field-sidekick. Keep changes small, explicit, testable, and consistent with the project's local-only safety model.

## Development setup

Python 3.13+ and uv are required:

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Use feature branches named for their purpose, for example `docs/provider-guide`, `feat/firefox-profile-check`, or `fix/profile-validation`. Keep commits in Conventional Commits style, such as `docs: explain custom profiles`, `feat: add provider check`, or `fix: reject invalid service scope`.

## Configuration changes

Components are focused YAML files included by a top-level profile. Add or change configuration only when its schema and provider behavior are clear. Keep package mappings explicit, avoid private paths and credentials, and leave account, vendor, remote, or device-dependent operations as `MANUAL` unless there is an approved narrow design.

Schema changes require updates to the Pydantic models, unit tests, configuration docs, examples, and bundled config. Preserve strict validation: unknown configuration keys should fail.

## Provider changes

Providers are built-in concrete code, not plugins. A new provider should be justified by a stable local action and include a support check, read-only state inspection, bounded application behavior, plan integration, tests, and documentation. Do not add dynamic discovery, remote enrollment, credential handling, or broad automation merely to make a provider generic.

## Pull requests

Before opening a PR, run the commands above and update docs for user-visible behavior. Describe the safety impact and show representative plan output when provider behavior changes.

PR checklist:

- [ ] Branch and commits are focused and use the expected naming/convention.
- [ ] `uv run ruff check .`, `uv run ruff format --check .`, and `uv run pytest` pass.
- [ ] Configuration/schema changes include tests and documentation.
- [ ] No secrets, credentials, private paths, or generated local artifacts are included.
- [ ] New automation has an explicit local scope, confirmation/dry-run behavior where appropriate, and documented manual boundaries.
