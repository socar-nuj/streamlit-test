from typing import Any, Dict


class Error(Exception):
    def __init__(self, title: str, detail: str = "") -> None:
        self.title = title
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.title}\n{f'detail: {self.detail}' if self.detail else ''}"

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}
