# TODO(humphrey / hardy): 이 모듈의 행방을 정해주세욥..!

# import logging
# import os
# from typing import Optional, Tuple
#
# import mlflow
#
# from somlier.application.ports.artifact_repository import (
#     ArtifactRepository,
#     MLflowModelMeta,
# )
# from somlier.application.ports.clients.mlflow_client import MLflowClient
#
#
# class MLflowModelNotFound(Exception):
#     pass
#
#
# class MLflowTrackingServerUnreachable(Exception):
#     pass
#
#
# class GCPCredentialNotFound(Exception):
#     pass
#
#
# class MLflowArtifactRepository(ArtifactRepository):
#     def __init__(self, mlflow_client: MLflowClient, artifact_directory_save_path: str) -> None:
#         self.mlflow_client = mlflow_client
#         self.artifact_directory_save_path = artifact_directory_save_path
#         self._logger = logging.getLogger(__name__)
#
#     def get(
#         self,
#         model_name: str,
#         model_version: str,
#         dir_path: Optional[str] = None,
#         **kwargs,
#     ) -> MLflowModelMeta:
#         """mlflow model artifact를 다운로드 합니다.
#
#         args:
#             model_name: str
#             model_version: str
#             dir_path: Optional[str]
#         returns:
#             ModelMeta
#         """
#         try:
#             model_meta = self._fetch_mlflow_model_info(model_name=model_name, model_version=model_version)
#             self._download_model_artifacts(model_meta=model_meta)
#             return model_meta
#         except ValueError as err:
#             raise GCPCredentialNotFound(err)
#
#     def _fetch_mlflow_model_info(self, model_name: str, model_version: str) -> MLflowModelMeta:
#         """MLflow Tracking 서버로 부터 모델 관련 정보를 받아 옵니다.
#
#         args:
#             model_name: str
#             model_version: str
#         returns:
#             mlflow.pyfunc.PyFuncModel
#         """
#         try:
#             model = self.mlflow_client.get_model_version(name=model_name, version=model_version)
#         except mlflow.exceptions.RestException:
#             self._logger.error("모델을 찾을 수 없습니다")
#             raise MLflowModelNotFound()
#
#         self._logger.info(f"MLflow로 부터 [{model.name}:{model.version}]를 가져왔습니다")
#         return MLflowModelMeta(pyfunc=mlflow.pyfunc.load_model(model_uri=model.source), source_uri=model.source)
#         # return MLflowModelMeta(
#         #         pyfunc=load_model(model_uri=model.source, map_location=torch.device("cpu")), # NOTE(humphrey): pytorch에서 cpu를 사용할 때 분기처리하도록 변경한다
#         #     source_uri=model.source,
#         # )
#
#     def _download_model_artifacts(
#         self, model_meta: MLflowModelMeta, local_dir: Optional[str] = None
#     ) -> Tuple[str, str]:
#         """model artifact를 mlflow로 부터 받아옵니다.
#
#         args:
#             pyfunc: mlflow.pyfunc.PyFuncModel
#             local_dir: Optional[str]
#         returns:
#             (str, str): local_path, model_artifact_path
#         """
#         if not local_dir:
#             local_dir = self.artifact_directory_save_path
#
#         # TODO(humphrey): remove local server storage usage
#         if not os.path.exists(local_dir):
#             os.mkdir(local_dir)
#         local_path = self.mlflow_client.download_artifacts(
#             run_id=model_meta.pyfunc.metadata.run_id, path=model_meta.pyfunc.metadata.artifact_path, dst_path=local_dir
#         )
#         model_artifact_path = model_meta.pyfunc.metadata.flavors.get("python_function").get("model_path")
#
#         return local_path, model_artifact_path
