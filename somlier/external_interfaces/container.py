import os
from typing import Optional

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI

from somlier.application.use_cases.offline.create import CreateBatch, CreateBatchV2
from somlier.application.use_cases.offline.list import ListBatches
from somlier.application.use_cases.online.cleanup.k8s_cleanup import K8SCleanup
from somlier.application.use_cases.online.deploy.k8s_deploy import K8SDeploy
from somlier.application.use_cases.online.deploy.local_deploy import LocalDeploy
from somlier.application.use_cases.online.register.handler import Register, RegisterV2
from somlier.application.use_cases.online.search import Search
from somlier.application.use_cases.online.train.handler import Train
from somlier.config import AppConfig, AppConfigEnv
from somlier.external_interfaces.outbound.clients.cli import CLIClient
from somlier.external_interfaces.outbound.clients.cli.bentoml_client import (
    BentoMLCLIClient,
)
from somlier.external_interfaces.outbound.clients.cli.dag_builder_client import (
    DAGBuilderCLIClient,
)
from somlier.external_interfaces.outbound.clients.cli.docker_client import (
    DockerCLIClient,
)
from somlier.external_interfaces.outbound.clients.rest.airflow_client import (
    AirflowRESTClient,
)
from somlier.external_interfaces.outbound.clients.rest.k8s_controller_client import (
    K8SControllerRESTClient,
)
from somlier.external_interfaces.outbound.clients.rest.mlflow_client import (
    MLflowRESTClient,
)
from somlier.external_interfaces.outbound.repositories.model_repository import (
    MLflowModelRepository,
)


def create_app() -> FastAPI:
    from ddtrace import patch

    from somlier.external_interfaces.inbound.web.exception_handler import (
        exception_handler,
    )
    from somlier.external_interfaces.inbound.web.offline_controller import (
        offline_router,
    )
    from somlier.external_interfaces.inbound.web.online_controller import online_router

    if os.getenv("ENV", "dev") == AppConfigEnv.PROD:
        patch(fastapi=True)

    app = FastAPI()
    app.include_router(online_router)
    app.include_router(offline_router)
    app.add_exception_handler(Exception, exception_handler)

    return app


class OnlineContainer(DeclarativeContainer):
    # dependencies
    config = providers.Configuration()

    # ports
    ## clients
    cli_client = providers.Singleton(CLIClient)
    bentoml_client = providers.Singleton(
        BentoMLCLIClient, cli_client=cli_client, default_bentoml_config_path=config.bentoml.config_path
    )
    docker_client = providers.Singleton(
        DockerCLIClient, registry_host=config.docker.cli.registry_host, cli_client=cli_client
    )
    k8s_controller_client = providers.Factory(K8SControllerRESTClient, host=config.k8s_controller.rest.host)
    mlflow_client = providers.Factory(
        MLflowRESTClient,
        mlflow_tracking_uri=config.mlflow.rest.tracking_uri,
        kube_context=config.mlflow.rest.kube_context,
        kube_config_path=config.mlflow.rest.kube_config_path,
        kube_repository_uri=config.mlflow.rest.kube_repository_uri,
        kube_job_template_path=config.mlflow.rest.kube_job_template_path,
        kube_job_with_gpu_template_path=config.mlflow.rest.kube_job_with_gpu_template_path,
    )

    ## repositories
    model_repository = providers.Singleton(MLflowModelRepository, mlflow_client=mlflow_client)

    # use_cases
    train = providers.Singleton(
        Train, mlflow_client=mlflow_client, default_project_uri=config.mlflow.default_project_uri
    )
    search = providers.Singleton(Search, mlflow_client=mlflow_client)
    register = providers.Singleton(Register, mlflow_client=mlflow_client)
    register_v2 = providers.Singleton(
        RegisterV2, mlflow_client=mlflow_client, default_project_uri=config.mlflow.default_project_uri
    )
    local_deploy = providers.Singleton(LocalDeploy, model_repository=model_repository, bentoml_client=bentoml_client)
    k8s_deploy = providers.Singleton(
        K8SDeploy,
        model_repository=model_repository,
        k8s_controller_client=k8s_controller_client,
        docker_client=docker_client,
        bentoml_client=bentoml_client,
    )
    deploy = providers.Dict(local=local_deploy, k8s=k8s_deploy)
    k8s_cleanup = providers.Singleton(K8SCleanup, k8s_controller_client=k8s_controller_client)


class OfflineContainer(DeclarativeContainer):
    # dependencies
    config = providers.Configuration()

    # ports
    ## client
    cli_client = providers.Singleton(CLIClient)
    airflow_client = providers.Factory(
        AirflowRESTClient,
        host=config.airflow.rest.host,
        headers=config.airflow.rest.headers,
        timeout=config.airflow.rest.timeout,
    )
    dag_builder_client = providers.Singleton(DAGBuilderCLIClient)

    # use_cases
    create = providers.Singleton(
        CreateBatch,
        airflow_client=airflow_client,
        mlops_dag_repo_url=config.airflow.default_dag_repo_url,
        dag_builder_client=dag_builder_client,
    )
    list = providers.Singleton(ListBatches, airflow_client=airflow_client)
    create_v2 = providers.Singleton(
        CreateBatchV2,
        airflow_client=airflow_client,
        mlops_dag_repo_url=config.airflow.default_dag_repo_url,
        dag_builder_client=dag_builder_client,
    )


class AppContainer(DeclarativeContainer):
    # dependencies
    config = providers.Configuration()
    online_container = providers.Container(OnlineContainer, config=config)
    offline_container = providers.Container(OfflineContainer, config=config)
    server_app: FastAPI = providers.Resource(create_app)


def create_container(config: Optional[AppConfig] = None) -> AppContainer:
    from somlier.external_interfaces.inbound.web import (
        offline_controller,
        online_controller,
    )

    if not config:
        config = AppConfig()
    container = AppContainer()
    container.config.from_pydantic(config)
    container.wire([online_controller, offline_controller])
    return container


class ConfigContainer(DeclarativeContainer):
    # dependencies
    config = providers.Configuration()
