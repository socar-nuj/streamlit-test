from somlier.core.exceptions import Error


class ExternalInterfaceError(Error):
    pass


class HealthcheckError(ExternalInterfaceError):
    pass


class ConnectionTimeoutError(ExternalInterfaceError):
    pass
