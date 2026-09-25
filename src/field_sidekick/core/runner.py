"""Narrow subprocess boundary so checks are easy to test."""

from dataclasses import dataclass
from subprocess import CompletedProcess, run


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class CommandRunner:
    def which(self, command: str) -> str | None:
        import shutil

        return shutil.which(command)

    def run(self, args: list[str], timeout: float = 3.0) -> CommandResult:
        try:
            result: CompletedProcess[str] = run(
                args, capture_output=True, text=True, timeout=timeout, check=False
            )
        except (OSError, TimeoutError) as error:
            return CommandResult(1, stderr=str(error))
        return CommandResult(result.returncode, result.stdout.strip(), result.stderr.strip())
