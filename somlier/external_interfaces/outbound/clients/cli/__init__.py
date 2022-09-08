import subprocess
from typing import List

from loguru import logger


class CLIClient:
    def __init__(self):
        self._logger = logger

    def create_subprocess(self, commands: List[str], should_print_output: bool = True):
        with subprocess.Popen(
            " ".join(commands),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            shell=True,
        ) as p:
            for stdout_line in p.stdout:
                if not stdout_line:
                    continue
                if should_print_output:
                    print(stdout_line)
            output, error = p.communicate()
            if p.returncode != 0:
                self._logger.error("서브 프로세스가 실패했습니다 %d %s %s" % (p.returncode, output, error))
            return output, error
