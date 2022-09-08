import collections
import os
import re
from typing import Any, Dict, Optional, Union

from somlier.config.exceptions import SoMLierConfigError

CONFIGURABLE_FILE_TYPE_WITH_EXTENSION_MAP = {"YAML": (".yaml", ".yml")}

FilePath = Union[os.PathLike, str]


class ReadableConfigFileNotFound(SoMLierConfigError):
    pass


class ConfigParseError(SoMLierConfigError):
    pass


class YAMLConfig:
    @staticmethod
    def parse(yaml_path: str) -> Dict[str, Any]:
        import yaml

        config: Dict[str, Any] = {}
        env_pattern = re.compile(r".*?\${(.*?)}.*?")

        def env_constructor(loader, node):
            value = loader.construct_scalar(node)
            for group in env_pattern.findall(value):
                splitted = group.split(":")
                env, default_value = splitted[0], ":".join(splitted[1:])
                value = value.replace(f"${{{group}}}", os.environ.get(env, default_value))
                continue
            return value

        yaml.add_implicit_resolver("!pathex", env_pattern)
        yaml.add_constructor("!pathex", env_constructor)

        with open(yaml_path, "r") as f:
            try:
                parsed_yaml = yaml.full_load(f)
            except yaml.YAMLError as exc:
                raise ConfigParseError(str(exc))

            if not parsed_yaml:
                return config
            config.update(parsed_yaml)
        return config


class Struct(object):
    def __init__(self, data: Dict[str, Any]) -> None:
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value: Any) -> Union["Struct", Any]:
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value

    def _dict(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, dict):
            return dict((key, self._dict(val)) for key, val in obj.items())
        elif isinstance(obj, collections.Iterable):
            return [self._dict(val) for val in obj]
        elif hasattr(obj, "__dict__"):
            return self._dict(vars(obj))
        return obj

    def dict(self) -> Dict[str, Any]:
        return self._dict(self)


def _get_file_type(file_path: FilePath) -> Optional[str]:
    default_file_type = None
    for file_type, extensions in CONFIGURABLE_FILE_TYPE_WITH_EXTENSION_MAP.items():
        if not file_path.endswith(extensions):
            continue

        return file_type
    return default_file_type


def configure(config_path: FilePath, *, as_struct: bool = False) -> Union[Dict[str, Any], Struct]:
    """
    file로 부터 config를 읽습니다

    :param config_path: config 파일의 경로
    :param as_struct: struct로 리턴할 지에 대한 여부
    :return: config
    """
    config: Dict[str, Any] = {}
    file_type = _get_file_type(config_path)
    if file_type == "YAML":
        parsed_config = YAMLConfig.parse(config_path)
        config.update(parsed_config)

    else:
        raise ReadableConfigFileNotFound(message=f"지원하지 않는 config 파일입니다 \tgot: [{config_path}]")

    if as_struct:
        struct_config = Struct(data=config)
        return struct_config

    return config
