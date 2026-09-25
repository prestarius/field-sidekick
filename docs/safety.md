# Safety model

Field-sidekick operates on the local workstation described by a reviewed profile. It makes intent visible before action: `field plan` is read-only and `field apply --dry-run` is read-only. A real apply renders the plan, requires confirmation by default, and applies only entries with an explicit provider action.

The project does not automate reconnaissance, scanning, exploitation, credential collection, password attacks, persistence, lateral movement, remote network changes, account login, remote enrollment, device pairing, or secret handling. A listed package is not an instruction to run it against any target.

Treat profiles as code. Review changes, keep private machine information and credentials out of tracked YAML, use a narrow scope during first application, and rerun `field plan` afterward. `--yes` is appropriate only in a reviewed, non-interactive workflow.

Unsupported platforms produce `SKIP` rows. They are not coerced into a guessed package or service action. Manual rows are intentionally non-actionable.

For vulnerability reporting, see [SECURITY.md](../SECURITY.md).
