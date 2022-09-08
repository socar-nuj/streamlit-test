
<p align="center">
  <img src="docs/images/soMLier_logo.png" width="300" />
</p>

<br>

<h1 id="sample-markdown" align="center">
SoMLier
</h1>

<div align="center">
쏘카의 MLOps - Serving 플랫폼, SoMLier
</div>

<br>

<div align="center">
<img src="https://app.buddy.works/socar/socar-data-somlier/pipelines/pipeline/327797/badge.svg?token=84ac990a8afcb41b597ff789b1a8edc1fdf4dd0811b98f2243d5dd3ce3b5af56" />
<img src="https://img.shields.io/badge/python-3.7%20%7C%203.8-blue">
<img src="https://github.com/socar-inc/socar-data-soMLier/actions/workflows/ci.yaml/badge.svg">
</div>


---
### Requirements
- Python >=3.7, <3.9
- SSH key for github organization

### 설치
1. SoMLier를 다운로드 합니다
    **pip 사용**
    ```shell
    $ pip install --user git+https://github.com/socar-inc/socar-data-soMLier.git@develop
    $ pip install --user git+https://github.com/socar-inc/socar-data-soMLier.git@$version이름
    ```

    **From source**
    ```shell
    # clone
    $ git clone git@github.com:socar-inc/socar-data-soMLier.git
    # or
    $ git clone https://github.com/socar-inc/socar-data-soMLier.git
    # and move to the directory
    $ cd socar-data-soMLier

    # install
    $ pip install -e .
    # or use poetry
    $ poetry install
    ```

2. 다음과 같은 환경변수들을 세팅합니다.

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

3. SoMLier를 사용합니다
  ```shell
  $ somlier version
  >> SoMLier v$current_version
  ```

### 링크
- SoMLier
  - 개발: http://somlier.mlops.socar.me/docs
  - 운영: TBD
- 모델 레지스트리
  - 개발: http://mlflow.mlops.socar.me
  - 운영: TBD
- 모델 개발
  - [ml-projects](https://github.com/socar-inc/socar-data-ml-projects)
- SoMLier 사용법 (구글 슬라이드)
  - [MLOps 설명 & 쏘믈리에(SoMLier) 사용법](https://docs.google.com/presentation/d/1hjM1fzYU11MFmCB_Gzh_spX9P00L5f_MAubi4Vcl0Xo/edit?usp=sharing)

### 문서 모음
- [사용법/유즈케이스](./docs/USECASES.md)
- [개발 관련](./docs/DEVELOPMENT.md)
- [아키텍쳐 관련](./docs/ARCHITECTURE.md)
- [테스트 관련](./docs/TESTS.md)
