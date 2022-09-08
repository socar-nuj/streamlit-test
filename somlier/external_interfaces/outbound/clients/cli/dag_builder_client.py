from typing import List

from clikit.args import StringArgs
from dag_builder.cmd.app import cli_app

from somlier.application.ports.clients.dag_builder_client import DAGBuilderClient
from somlier.core.exceptions import Error


class DAGBuilderCLIClientValueError(Error):
    pass


class DAGBuilderCLIClient(DAGBuilderClient):
    def __init__(self):
        self.app = cli_app()

    @property
    def can_use(self) -> bool:
        try:
            from dag_builder.cmd.app import cli_app
        except ImportError:
            return False
        return True

    def generate(self, args: List[str]) -> str:
        try:
            stringified_args = " ".join(args)
            stringified_args = stringified_args.replace("'", '"')

            result = self._catch_stdout(stringified_args=stringified_args)
            # MEMO: socar-data-dag-builder에서 stdout에 '...이미지를 DAG로 만듭니다' 문자열이 포함되어 있어 firstline을 제거합니다.
            return "\n".join(result.splitlines()[1:])
        except ValueError as e:
            raise DAGBuilderCLIClientValueError(title="올바르지 않은 docker image input 입니다", detail=str(e))
        except Exception:
            raise

    def _catch_stdout(self, stringified_args: str) -> str:
        """
        stdout을 String 변수로 리디렉션합니다.
        @param stringified_args: stringified Arguments
        @return: Dag String
        """
        import io
        from contextlib import redirect_stdout

        with io.StringIO() as buf, redirect_stdout(buf):
            self.app.run(args=StringArgs(stringified_args))
            return buf.getvalue()
