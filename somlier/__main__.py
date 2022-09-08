import fire

from somlier import cli_name
from somlier.config import AppConfig
from somlier.external_interfaces.container import create_container
from somlier.external_interfaces.inbound.cli import MainController


def main():
    config = AppConfig()
    container = create_container(config=config)
    fire.Fire(MainController(container=container), name=cli_name)


if __name__ == "__main__":
    main()
