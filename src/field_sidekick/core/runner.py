"""Small subprocess boundary that is easy to mock in tests."""

from dataclasses import dataclass
import shutil
import subprocess


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
        return shutil.which(command)

    def run(self, *args: str, timeout: float = 3.0) -> CommandResult:
        try:
            completed = subprocess.run(
                args,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return CommandResult(returncode=127, stderr=str(exc))

        return CommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
        )
