# TODO(humphrey / hardy): 이 모듈의 행방을 정해주세욥..!

import importlib
import os

import mlflow.pyfunc.utils
from mlflow.exceptions import MlflowException
from mlflow.models.model import MLMODEL_FILE_NAME, Model
from mlflow.pyfunc import (
    CODE,
    DATA,
    FLAVOR_NAME,
    MAIN,
    PY_VERSION,
    PyFuncModel,
    _warn_potentially_incompatible_py_version_if_necessary,
)
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.rest_utils import RESOURCE_DOES_NOT_EXIST


def load_model(model_uri: str, suppress_warnings: bool = True, **kwargs) -> PyFuncModel:
    """
        Load a model stored in Python function format.
    m
        :param model_uri: The location, in URI format, of the MLflow model. For example:

                          - ``/Users/me/path/to/local/model``
                          - ``relative/path/to/local/model``
                          - ``s3://my_bucket/path/to/model``
                          - ``runs:/<mlflow_run_id>/run-relative/path/to/model``
                          - ``models:/<model_name>/<model_version>``
                          - ``models:/<model_name>/<stage>``

                          For more information about supported URI schemes, see
                          `Referencing Artifacts <https://www.mlflow.org/docs/latest/concepts.html#
                          artifact-locations>`_.
        :param suppress_warnings: If ``True``, non-fatal warning messages associated with the model
                                  loading process will be suppressed. If ``False``, these warning
                                  messages will be emitted.
    """
    local_path = _download_artifact_from_uri(artifact_uri=model_uri)
    model_meta = Model.load(os.path.join(local_path, MLMODEL_FILE_NAME))

    conf = model_meta.flavors.get(FLAVOR_NAME)
    if conf is None:
        raise MlflowException(
            'Model does not have the "{flavor_name}" flavor'.format(flavor_name=FLAVOR_NAME),
            RESOURCE_DOES_NOT_EXIST,
        )
    model_py_version = conf.get(PY_VERSION)
    if not suppress_warnings:
        _warn_potentially_incompatible_py_version_if_necessary(model_py_version=model_py_version)
    if CODE in conf and conf[CODE]:
        code_path = os.path.join(local_path, conf[CODE])
        mlflow.pyfunc.utils._add_code_to_system_path(code_path=code_path)
    data_path = os.path.join(local_path, conf[DATA]) if (DATA in conf) else local_path
    model_impl = importlib.import_module(conf[MAIN])._load_pyfunc(data_path, **kwargs)
    # model_impl = importlib.import_module(conf[MAIN])._load_pyfunc(data_path)
    return PyFuncModel(model_meta=model_meta, model_impl=model_impl)
