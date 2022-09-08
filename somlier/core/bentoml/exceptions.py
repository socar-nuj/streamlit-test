from somlier.core.exceptions import Error


class NotFoundError(Error):
    pass


class ArtifactUnknownExtensionError(Error):
    pass


class ArtifactFileNotFoundError(NotFoundError):
    pass
