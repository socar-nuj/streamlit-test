from somlier.external_interfaces.container import AppContainer
from somlier.external_interfaces.inbound.cli.offline_controller import OfflineController
from somlier.external_interfaces.inbound.cli.online_controller import OnlineController
from somlier.external_interfaces.inbound.cli.config_controller import ConfigController


class MainController:
    def __init__(self, container: AppContainer) -> None:
        self.online = OnlineController(container=container.online_container)
        self.offline = OfflineController(container=container.offline_container)
        self.config = ConfigController(container=container.config)

    def version(self) -> str:
        import somlier

        return f"SoMLier v{somlier.__version__}"
