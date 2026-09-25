"""Helpers shared by built-in modules."""

from field_sidekick.core import CheckResult, CheckStatus, SidekickContext


def command_result(context: SidekickContext, module: str, name: str, command: str) -> CheckResult:
    path = context.runner.which(command)
    return CheckResult(
        module, name, CheckStatus.PASS if path else CheckStatus.WARN, path or "not installed"
    )
