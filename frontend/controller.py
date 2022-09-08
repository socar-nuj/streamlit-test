from somlier.config import AppConfig
from somlier.external_interfaces.container import create_container

config = AppConfig()
container = create_container(config=config)
online_container = container.online_container
offline_container = container.offline_container
