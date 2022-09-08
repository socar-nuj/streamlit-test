import subprocess
import threading
from subprocess import PIPE, Popen
from typing import Sequence

import pytest


def test_somlier_import():
    try:
        import somlier
    except ImportError:
        assert False

    assert True


def test_somlier_cli_version_command(caplog):
    process = subprocess.Popen("somlier version", shell=True, stdout=PIPE)
    stdout, stderr = process.communicate()
    assert "SoMLier v" in stdout.decode("utf-8")


class SoMLierOnlineServerInThread(object):
    def __init__(self, cmd: Sequence[str]):
        self.cmd = cmd
        self.process: Popen[str] = None

    def run(self, timeout=0, **kwargs):
        def target(**kwargs):
            self.process = subprocess.Popen(self.cmd, **kwargs)
            self.process.communicate()

        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        return {"return_code": self.process.returncode}


@pytest.fixture
def run_somlier_online_server():
    online_server = SoMLierOnlineServerInThread(cmd=["somlier", "online", "server"])
    try:
        yield online_server.run(timeout=3)
    finally:
        online_server.process.terminate()


def test_somlier_rest_api_server_start(run_somlier_online_server):
    assert run_somlier_online_server["return_code"] == 0
