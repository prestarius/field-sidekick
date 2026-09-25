# Workstation notes

The target is a Kali Linux X1 field workstation, while the toolkit remains portable enough for development on another operating system. Linux-specific checks report `SKIP` or `WARN` on macOS rather than treating that development environment as broken.

Recommended workflow:

1. Install Python 3.13+ and uv.
2. Run `uv sync --all-groups`.
3. Review the desired state with `uv run field config show`.
4. Use `uv run field doctor` or `uv run field doctor wireless` to review local prerequisites.
5. Use `uv run field inventory` when documenting the machine.

The tool does not install packages, change network settings, manage browser profiles, scan networks, or contact remote services. A future apply workflow must be explicit and confirmed by the operator.
