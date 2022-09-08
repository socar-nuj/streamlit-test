from somlier.application.exceptions import NotFoundError, AlreadyExistError, ApplicationError, InvalidParameterError


class MLflowRunNotFoundError(NotFoundError):
    pass


class AlreadyReigsteredModel(AlreadyExistError):
    pass


class MLflowProjectNotFoundError(NotFoundError):
    pass


class MLflowRuntimeError(ApplicationError):
    pass


class InvalidTargetDirectoryError(InvalidParameterError):
    pass


class UnsupportedModelTypeError(InvalidParameterError):
    pass


class ArtifactNotFoundInGCSError(NotFoundError):
    pass


class PytorchModuleFileNotFoundError(NotFoundError):
    pass


class EmptyProjectParameterError(InvalidParameterError):
    pass


class PytorchModuleClassNotFoundError(NotFoundError):
    pass


class LoadPytorchWeightsRuntimeError(ApplicationError):
    pass


class SklearnPackageNotFoundError(NotFoundError):
    pass


class SklearnModuleClassNotFoundError(NotFoundError):
    pass


class InvalidSklearnModelError(InvalidParameterError):
    pass


class GitRepositoryNotFoundError(NotFoundError):
    pass
