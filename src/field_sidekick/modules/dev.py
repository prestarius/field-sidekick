"""Developer-tool checks."""

from field_sidekick.core.models import Check, CheckResult, CheckStatus
from field_sidekick.core.module import SidekickModule


class DevModule(SidekickModule):
    name = "dev"
    description = "Developer tooling"

    def checks(self) -> list[Check]:
        return [
            Check("dev.git", "Git", lambda: self._binary("git", required=True)),
            Check("dev.uv", "uv", lambda: self._binary("uv", required=True)),
            Check("dev.docker", "Docker CLI", lambda: self._binary("docker", required=False)),
            Check("dev.docker-daemon", "Docker daemon", self._docker_daemon),
        ]

    def _binary(self, command: str, *, required: bool) -> CheckResult:
        path = self.runner.which(command)
        status = (
            CheckStatus.PASS
            if path
            else (CheckStatus.FAIL if required else CheckStatus.WARN)
        )
        return CheckResult(f"dev.{command}", command, status, path or "not found")

    def _docker_daemon(self) -> CheckResult:
        if not self.runner.which("docker"):
            return CheckResult(
                "dev.docker-daemon",
                "Docker daemon",
                CheckStatus.SKIP,
                "Docker CLI not installed",
            )

        result = self.runner.run("docker", "info", "--format", "{{.ServerVersion}}")
        if result.ok:
            return CheckResult(
                "dev.docker-daemon",
                "Docker daemon",
                CheckStatus.PASS,
                f"reachable, server {result.stdout or 'unknown'}",
            )

        return CheckResult(
            "dev.docker-daemon",
            "Docker daemon",
            CheckStatus.WARN,
            result.stderr or "daemon unavailable or current user lacks access",
        )
