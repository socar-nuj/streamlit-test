class SoMLierConfigError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}" f"Traceback: {self.__traceback__}"
