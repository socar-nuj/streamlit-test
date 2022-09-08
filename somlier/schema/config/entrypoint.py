from typing import Union, List, Optional

from somlier.schema.config.common import BaseSchema


class SomlierEntrypoint(BaseSchema):
    command: Union[List[str], str]
    args: Optional[List[str]]

    def to_command_line(self):
        return " ".join(self.to_args())

    def to_args(self):
        return [] + self.command if isinstance(self.command, list) else self.command.split() + (self.args or [])

    def validate_(self):
        entrypoint = self.to_args()
        # TODO: validate command
        return any(entrypoint)
