# CLI reference

All commands accept `--profile PATH_OR_NAME` where shown. Explicit paths win; named profiles resolve from the user config directory before bundled templates. The default is the user `x1-kali` profile when initialized, otherwise the bundled read-only X1/Kali template.

| Command | Purpose | Changes state? |
| --- | --- | --- |
| `field doctor [MODULE]` | Run local checks; module is `system`, `dev`, `network`, or `wireless` | No |
| `field inventory` | Print local machine and tool summary | No |
| `field modules list` | List built-in diagnostic modules | No |
| `field config path` | Show user config directory and active profile | No |
| `field config init [--force]` | Copy bundled starter YAML locally; `--force` replaces starter files | Local files only |
| `field config validate` | Validate selected profile and components | No |
| `field config show` | Print the loaded desired-state profile as JSON | No |
| `field plan [SCOPE]` | Compare desired state with local state | No |
| `field apply [SCOPE] [--dry-run] [--yes]` | Confirm and perform actionable plan entries | Yes, except `--dry-run` |

Examples:

```bash
field --version
field config init
field config validate
field doctor wireless
field config show --profile x1-kali
field plan dev
field apply firefox --dry-run
field apply packages --yes
```

`plan` and `apply` take either a component name or `packages`. Unknown scopes and unknown doctor modules are errors. `apply` renders the plan before confirmation. Its `--yes` flag bypasses only the confirmation prompt; it does not make `MANUAL` or unsupported entries actionable.
