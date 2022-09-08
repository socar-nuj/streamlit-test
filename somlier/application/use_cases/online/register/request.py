from typing import Optional

from pydantic import BaseModel, validator

from somlier.application.use_cases.online.register.exceptions import (
    UnsupportedModelTypeError,
    EmptyProjectParameterError,
)

VALID_SKLEARN_MODEL_TYPE = ("sklearn", "scikit-learn")
VALID_PYTORCH_MODEL_TYPE = ("pytorch", "torch")
VALID_MODEL_TYPE = VALID_SKLEARN_MODEL_TYPE + VALID_PYTORCH_MODEL_TYPE


class RegisterRequest(BaseModel):
    run_id: str
    model_name: str


class RegisterRequestV2(BaseModel):
    model_type: str
    gcs_uri: str
    model_name: str
    project_uri: Optional[str]
    project_name: Optional[str]
    project_ref: Optional[str]
    model_module_path: Optional[str]
    model_class_name: Optional[str]

    @validator("model_type")
    def model_type_must_be_in_valid_type(cls, v):
        """model_type 인자가 정해진 값 안에 포함되는지 확인한다."""

        if v not in VALID_MODEL_TYPE:
            raise UnsupportedModelTypeError(
                title="지원하지 않는 모델 타입입니다.",
                detail="somlier online register_v2는 sklearn(scikit-learn), pytorch(torch) 모델을 지원합니다.",
            )
        return v

    @validator("project_uri", "project_name", "project_ref", "model_module_path", "model_class_name")
    def pytorch_model_type_must_have_project(cls, v, values):
        """pytorch 모델의 경우 github project 관련된 인자들이 입력되었는지 확인한다."""

        if values["model_type"] in VALID_PYTORCH_MODEL_TYPE and not v:
            raise EmptyProjectParameterError(
                title="pytorch 모델의 등록을 위해서는 모델 클래스가 정의된 github project repository 정보가 필요합니다."
            )
        return v
