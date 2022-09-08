from somlier.core.exceptions import Error


class ApplicationError(Error):
    pass


class ClientError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass


class AlreadyExistError(ApplicationError):
    pass


class InvalidParameterError(ApplicationError):
    pass
