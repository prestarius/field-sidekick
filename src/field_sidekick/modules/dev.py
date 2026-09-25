"""Local development-tool checks."""

from field_sidekick.core import Check, CheckResult, CheckStatus, SidekickContext, SidekickModule
from field_sidekick.modules.common import command_result


class DevModule(SidekickModule):
    name = "dev"
    description = "Python, Git, uv, and Docker readiness"

    def checks(self, context: SidekickContext) -> tuple[Check, ...]:
        return (
            Check("Python 3.13+", self._python),
            Check("Git", lambda c: command_result(c, self.name, "Git", "git")),
            Check("uv", lambda c: command_result(c, self.name, "uv", "uv")),
            Check("Docker", self._docker),
        )

    def _python(self, context: SidekickContext) -> CheckResult:
        value = context.platform.info().python_version
        major, minor = (int(part) for part in value.split(".")[:2])
        status = CheckStatus.PASS if (major, minor) >= (3, 13) else CheckStatus.FAIL
        return CheckResult(self.name, "Python 3.13+", status, value)

    def _docker(self, context: SidekickContext) -> CheckResult:
        if not context.runner.which("docker"):
            return CheckResult(self.name, "Docker", CheckStatus.WARN, "not installed")
        result = context.runner.run(["docker", "info", "--format", "{{.ServerVersion}}"])
        if result.ok:
            return CheckResult(
                self.name, "Docker", CheckStatus.PASS, f"daemon reachable (server {result.stdout})"
            )
        return CheckResult(
            self.name,
            "Docker",
            CheckStatus.WARN,
            "installed, but daemon unavailable or access denied",
        )
