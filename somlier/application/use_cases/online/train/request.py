import re
from typing import Optional, Dict, Any

from pydantic import BaseModel, validator

from somlier.application.use_cases.online.train.exceptions import InvalidParamsFormatError

VALID_CONTINUOUS_REGEX_FORMAT = r"(([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)|([0-9]+))\.\.(([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)|([0-9]+))\.\.(([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)|([0-9]+))"
VALID_DISCRETE_REGEX_FORMAT = r"(?!.*(\.\.))(.+?)(?:,|$)"
VALID_SINGLE_REGEX_FORMAT = r"(?!.*,)(?!.*(\.\.)).*"


class TrainRequest(BaseModel):
    project_uri: Optional[str]
    project_name: Optional[str]
    project_version: Optional[str]
    project_ref: Optional[str] = "main"
    project_entrypoint: str = "main"
    use_k8s_job: bool = True
    use_gpu: bool = False
    params: Optional[Dict[str, Any]] = None

    @validator("project_name")
    def validate_project_name(cls, v, values, **kwargs):
        if not v:
            if "#" in values["project_uri"]:
                return values["project_uri"].split("#")[-1]
            else:
                return values["project_uri"].split("/")[-1]
        return v

    @validator("params")
    def validate_params(cls, v: Optional[Dict[str, Any]]):
        if not v:
            return v

        for param_name, param_values in v.items():
            if isinstance(param_values, tuple):
                param_values = ",".join([str(pv) for pv in param_values])
            else:
                param_values = str(param_values)
            if (
                not re.fullmatch(VALID_CONTINUOUS_REGEX_FORMAT, param_values)  # {start}..{end}..{increment}
                and not re.fullmatch(VALID_DISCRETE_REGEX_FORMAT, param_values)  # {value1},{value2},{value3}...
                and not re.fullmatch(VALID_SINGLE_REGEX_FORMAT, param_values)  # {value}
            ):
                raise InvalidParamsFormatError(
                    title=f"올바른 파라미터 형태가 아닙니다. [{param_values}]",
                    detail="Required: type=start..end..increment or type=value1,value2,value3 or type=value",
                )

            v[param_name] = param_values.replace(" ", "")

        return v
