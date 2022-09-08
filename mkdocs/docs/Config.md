## Config


| category |                 key                  |     default value     |        description         |                    example                    |
|:--------:|:------------------------------------:|-----------------------|:--------------------------:|:---------------------------------------------:|
| Airflow  |        SOMLIER__AIRFLOW__HOST        |                       |      Airflow Host URL      |        https://airflow.mlops.socar.me         |
|          |      SOMLIER__AIRFLOW__USERNAME      |                       |      Airflow Username      |                     admin                     |
|          |      SOMLIER__AIRFLOW__PASSWORD      |                       |      Airflow Password      |                     socar                     |
|          |      SOMLIER__AIRFLOW__TIMEOUT       |           5           | Airflow Connection Timeout |                       1                       |
| BentoML  |    SOMLIER__BENTOML__CONFIG_PATH     |                       |    BentoML Config Path     |                  ~/.bentoml                   |
|  Docker  |    SOMLIER__DOCKER__REGISTRY_HOST    | gcr.io/socar-data-dev |   Docker Image Host Name   |             gcr.io/socar-data-dev             |
| K8S CTRL |  SOMLIER__K8S_CONTROLLER_REST_HOST   |                       |  K8S Controller Host Name  | http://somlier-k8s-controller.mlops.socar.me/ |
|  MLflow  |    SOMLIER__MLFLOW__TRACKING_URI     |                       |    MLflow Tracking URI     |         https://mlflow.mlops.socar.me         |
|          |  SOMLIER__MLFLOW__KUBE_CONFIG_PATH   |                       |   Kubernetes Config Path   |                ~/.kube/config                 |
|          | SOMLIER__MLFLOW__KUBE_REPOSITORY_URI |                       |          GCR URI           |         gcr.io/socar-data-dev/somlier         |

