# Workstation notes

The initial target is a Kali Linux field workstation, but v0.1 remains portable enough to run on another operating system. Missing Linux-specific indicators, such as Wi-Fi interfaces under `/sys/class/net`, are reported rather than treated as errors.

Recommended workflow:

1. Install Python 3.13+ and uv.
2. Run `uv sync --all-groups`.
3. Use `uv run field doctor` to review local prerequisites.
4. Use `uv run field inventory` when documenting the machine.

The tool does not install packages, change network settings, manage browser profiles, or contact remote services.
