from typing import TYPE_CHECKING

from pydantic import BaseModel, BaseSettings

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny


class PropertyBaseModel(BaseModel):
    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """

    def __init__(self, **data):
        super().__init__(**data)
        for getter, setter in self.get_properties():
            if getter in data and setter:
                getattr(type(self), setter).fset(self, data[getter])

    @classmethod
    def get_properties(cls):
        attributes = {prop: getattr(cls, prop) for prop in dir(cls)}
        properties = {
            name: attribute
            for name, attribute in attributes.items()
            if isinstance(attribute, property) and name not in ("__values__", "fields")
        }

        setters = {prop.fget: name for name, prop in properties.items() if prop.fset}
        return [(name, setters.get(prop.fget)) for name, prop in properties.items() if prop.fget and not prop.fset]

    def dict(self, *args, **kwargs) -> "DictStrAny":
        self.__dict__.update({getter: getattr(self, getter) for getter, setter in self.get_properties()})

        return super().dict(*args, **kwargs)


class PropertyBaseSettings(BaseSettings):
    def __init__(self, **data):
        super().__init__(**data)
        for getter, setter in self.get_properties():
            if getter in data and setter:
                getattr(type(self), setter).fset(self, data[getter])

    @classmethod
    def get_properties(cls):
        attributes = {prop: getattr(cls, prop) for prop in dir(cls)}
        properties = {
            name: attribute
            for name, attribute in attributes.items()
            if isinstance(attribute, property) and name not in ("__values__", "fields")
        }

        setters = {prop.fget: name for name, prop in properties.items() if prop.fset}
        return [(name, setters.get(prop.fget)) for name, prop in properties.items() if prop.fget and not prop.fset]

    def dict(self, *args, **kwargs) -> "DictStrAny":
        self.__dict__.update({getter: getattr(self, getter) for getter, setter in self.get_properties()})

        return super().dict(*args, **kwargs)


class DefaultSettings(PropertyBaseSettings):
    class Config:
        env_file = ".env"
