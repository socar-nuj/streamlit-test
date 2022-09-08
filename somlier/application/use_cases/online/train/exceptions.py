from somlier.application.exceptions import NotFoundError, AlreadyExistError, ApplicationError, InvalidParameterError


class InvalidParamsFormatError(InvalidParameterError):
    pass


class ParamsTypeCastError(InvalidParameterError):
    pass


class InvalidContinuousParamError(InvalidParameterError):
    pass


class EmptyParamsError(InvalidParameterError):
    pass
