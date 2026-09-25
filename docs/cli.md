# CLI reference

All commands accept `--profile PATH` where shown; the default is `configs/profiles/x1-kali.yaml`.

| Command | Purpose | Changes state? |
| --- | --- | --- |
| `field doctor [MODULE]` | Run local checks; module is `system`, `dev`, `network`, or `wireless` | No |
| `field inventory` | Print local machine and tool summary | No |
| `field modules list` | List built-in diagnostic modules | No |
| `field config show` | Print the loaded desired-state profile as JSON | No |
| `field plan [SCOPE]` | Compare desired state with local state | No |
| `field apply [SCOPE] [--dry-run] [--yes]` | Confirm and perform actionable plan entries | Yes, except `--dry-run` |

Examples:

```bash
uv run field doctor wireless
uv run field config show --profile configs/profiles/x1-kali.yaml
uv run field plan dev
uv run field apply firefox --dry-run
uv run field apply packages --yes
```

`plan` and `apply` take either a component name or `packages`. Unknown scopes and unknown doctor modules are errors. `apply` renders the plan before confirmation. Its `--yes` flag bypasses only the confirmation prompt; it does not make `MANUAL` or unsupported entries actionable.
