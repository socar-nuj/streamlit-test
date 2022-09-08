import os
import subprocess
from typing import Callable, List

from termcolor import colored

from somlier.application.use_cases.config.operations import load_somlier
from somlier.external_interfaces.container import ConfigContainer


class ConfigController:
    def __init__(self, container: ConfigContainer) -> None:
        self.container = container

    def show(self, base: str = os.getcwd(), file: str = "", dependencies: bool = False) -> None:
        """Somlier config를 조회합니다"""

        _somlier, somlier_path = load_somlier(base_dir=base, file_path=file)

        call_somlier_ascii()

        if dependencies:
            deps = "\n".join([req.requirement.rstrip() for req in _somlier.dependencies])
            print(colored("-------- dependencies --------", "green"))
            print(colored(f"{deps}", "green"))
            print(colored("------------------------------", "green"))
            return

        print(colored("-------- SoMLier configs --------", "green"))
        print(colored("SoMLier YAML:", "green"), somlier_path)
        print(colored("Model Name: ", "green"), _somlier.model.name)
        print(colored("Model Versions: ", "green"), _somlier.model.version)
        print(colored("Model Tag: ", "green"), _somlier.model.tags)
        print(colored("Model Assets: ", "green"), _somlier.asset_names)
        print(colored("Python Versions: ", "green"), _somlier.project.python.version)
        print(
            colored("Docker Image Name: ", "green"), f"{_somlier.project.docker.name}:{_somlier.project.docker.tags}"
        )
        print(colored("---------------------------------", "green"))

    def run(self, entrypoint: str, base: str = os.getcwd(), file: str = "", logging_format: str = None) -> None:
        """SODA Project에 선언된 entrypoint를 실행합니다."""

        _somlier, _ = load_somlier(base_dir=base, file_path=file)
        if logging_format:
            _somlier.global_config.logging.format = logging_format
        entrypoint_to_run = _somlier.entrypoints.get(entrypoint)
        if not entrypoint_to_run:
            raise ValueError(f"[{entrypoint}] entrypoint를 찾을 수 없습니다.")
        call_somlier_ascii()
        print(colored(f"Entrypoint: [{entrypoint}] 을/를 실행합니다.", "green"))
        logging_handler = _somlier.get_log_handler()
        execute_in_subprocess(args=entrypoint_to_run.to_args(), name=entrypoint, logging_handler=logging_handler)


def execute_in_subprocess(args: List[str], name: str = "", logging_handler: Callable[[str, str], str] = None):
    print(colored(f"Executing {args}...", "green"))
    with subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=dict(os.environ, ANSIBLE_FORCE_COLOR="true", PYTHONUNBUFFERED="1"),
    ) as p:
        for stdout_line in p.stdout:
            if not stdout_line:
                continue
            logging_entry = logging_handler(stdout_line.decode("utf-8"), name)
            print(logging_entry)


def call_somlier_ascii():
    print(
        colored(
            """
          _____       __  _____    _
         / ___/____  /  |/  / /   (_)__  _____
         \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
        ___/ / /_/ / /  / / /___/ /  __/ /
       /____/\____/_/  /_/_____/_/\___/_/
    """,
            "red",
        )
    )
