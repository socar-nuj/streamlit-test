# Tutorial

## 개요

- MLOps Platform 을 통해 ML 모델을 생성, 실험, 배포하는 전체 LifeCycle을 경험해보는 것을 목표로 합니다.
- Offline Serving 까지의 과정은 개발 환경(socar-data-dev)에서 진행됩니다.
- Online Serving 과정은 운영 환경(socar-data)에서 진행됩니다.

## Brewery 를 이용해 작업 전용 서버(노트북)를 실행

### Brewery 란

- **주피터 노트북을 쉽게 사용/관리할 수 있도록 도와주는 서비스**
- 데이터플랫폼팀에서 관리하는 쿠버네티스 클러스터에서 운영되고 있습니다.
 
<p align="center">
  <img src="../images/brewery_1.png" width="100%" />
</p>


    Brewery 주소 : http://brewery.mlops.socar.me/hub 
<br>

### What is Role?

- 쉽고 빠르게 원하는 리소스의 작업 환경(노트북 서버)를 띄울 수 있습니다.
- 한 명의 사용자가 여러 개의 노트북 서버를 용도에 맞게 띄울 수 있습니다.
- 모델을 쉽게 실험&배포할 수 있습니다.(with. SoMLier)


### Brewery 작업 프로세스
1. VPN 연결
    - `AWS_DEV_VPN` 을 연결
    <p align="center">
      <img src="../images/brewery_2.png" width="30%" />
    </p>
   

2. 권한받기
    - `#ask_data_platform` 채널에 `Google 계정 이름` 과 `사용 용도`와 함께 권한을 요청합니다.

3. 로그인
    - `http://brewery.mlops.socar.me/` 로 접속
    - 쏘카 구글 계정으로 로그인합니다.

4. 노트북 서버 생성
    - `Add New Server`에 서버 이름 입력합니다.(사용 목적을 포함하면 관리하기 용이합니다)
    - 리소스를 선택합니다
    <p align="center">
      <img src="../images/brewery_6.png" width="100%" />
    </p>
    - 이미지 유형 선택
        - `기본`
    - 서버 기본 리소스 타입
        - `CPU 4 Core / Memory 16G`
        - `CPU 8 Core / Memory 32G`
    - Disk 선택 : Gi 단위로 작성
    - GPU 타입
        - `nvidia-tesla-p100`
        - `nvidia-tesla-v100`
        - `nvidia-tesla-t4`
    - GPU 갯수 : 1, 2, 4

    `GPU 노드의 비용 절감을 위해, GPU 갯수는 한 번 더 고민해보고 선택해주세요!` 

5. 노트북 서버 사용
    <p align="center">
      <img src="../images/brewery_8.png" width="100%" />
    </p>

    - 작업은 홈 디렉토리(`/home/jovyan`)에서 이뤄집니다
    - 모델 개발, 실험, 학습 등 ML 모델 관련 작업은 `socar-data-ml-projects/`에서 진행하시면 됩니다 <br>([ML-project 가이드](./ML_Project.md))
    - 노트북 서버 간 파일을 공유하고 싶을 때는 `shared/` 를 활용합니다.
        - `all` : 모든 사용자가 접근할 수 있습니다.
        - `users` : 사용자 별 공유 공간으로 사용합니다. (사용자가 직접 본인의 폴더를 만들어 사용)
          <p align="center">
          <img src="../images/brewery_9.png" width="100%" />
          </p>
    
6. 가상환경 설정 및 패키지 설치
    - 노트북 파이썬 버전은 `3.8.10` 이며 `pyenv` 로 관리되고 있습니다.
    - 새로운 파이썬 패키지를  설치하고 싶다면, 홈 디렉토리(/home/jovyan)에서 venv 가상환경을 만들어준 다음 설치해주세요. 
    
            $ cd /home/jovyan
            $ python -m venv .venv --system-site-packages
            $ source .venv/bin/activate
   
            (.venv)$ pip install some_package

    - `-system-site-packages` : 루트 파이썬 패키지들을 가상환경에서 쓸 수 있도록 설치하는 옵션
    - 가상환경이 아닌 곳에서 파이썬 패키지를 설치하면 서버가 내려간 후 재설치되었을 시 패키지가 삭제됩니다.
   
7. gsutill 설정
    - gcs 사용을 위해 gsutill 설정을 합니다.
   
            # 1. gsutil 설정을 하기 위한 커맨드를 입력합니다. 
            $ gcloud init --console-only
            # 2. 가이드에 따라 쏘카 구글 계정으로 로그인하고 코드를 붙여넣습니다.

            # 3. cloud project를 socar-data-dev로 입력합니다.

            # 4. default zone 설정은 no를 해줍니다

            # 5. 잘 동작하는지 테스트해봅니다. 
            $ gsutil du -s gs://socar-data-dev-ai # 해당 버킷의 총 용량을 확인합니다. 

8. 노트북 서버 중지/삭제
    - 서버 비용 절감을 위해 `30분` 동안 서버를 사용하지 않으면 자동으로 내려갑니다

    - 실행 서버에서 `stop` 버튼을 누르면 노트북 서버가 종료됩니다.
    <p align="center">
      <img src="../images/brewery_10.png" width="100%" />
    </p>

    - 재시작할 경우 `start` 를 누릅니다.
    <p align="center">
      <img src="../images/brewery_11.png" width="100%" />
    </p>
    - 재실행 시 서버 리소스를 다시 선택할 수 있습니다. (단, 디스크 볼륨은 수정이 불가합니다)
    - 서버를 영구적으로 삭제하고 싶으면 `delete` 를 눌러줍니다. (디스크 볼륨이 영구적으로 삭제됩니다)

    **주의** <br>
    - 노트북 서버가 종료(stop)되면 홈 디렉토리(/home/jovyan/*)를 제외한 파일들은 보존되지 않습니다.

    - 유지 되는 것
        - 홈 디렉토리(/home/jovyan)에 설치하는 모든 것
    - 유지되지 않는 것
        - 시스템 패키지(apt-get install)
        - 홈 디렉토리 바깥에서 설치되는 모든 것
        - 환경변수, 프로세스 실행 등


## ML프로젝트 생성하기

### ML-Project 란
- 쏘카 데이터 그룹에서 개발 및 운영하는 ML 프로젝트 저장소입니다.
- MLOps 도메인에서 사용하는 모든 ML 관련 프로젝트들은 하나의 프로젝트 저장소에 동일한 프로젝트 포멧으로 관리됩니다.
<br>
<br>

### What is Role?
- 하나의 프로젝트 저장소를 사용하여, 프로젝트 목록을 한 눈에 보고 검색할 수 있도록 합니다.
- 프로젝트의 변경사항이 모두에게 공유됩니다.
- 동일한 프로젝트 포맷을 통해, 일관된 프로젝트 구조로 보는 이에게 빠른 이해를 돕습니다.
- 또한 프로젝트 포맷은 “서빙"에도 최적화되어 있습니다. 포맷만 잘 지키면 서빙을 위한 별도의 작업을 하지 않아도 됩니다.


### ML-Project 작업 프로세스
1. github Repo 를 clone 받습니다.

        $ git clone git@github.com:socar-inc/socar-data-ml-projects.git

2. 프로젝트를 생성합니다.
        
        $ cd socar-data-ml-projects
        $ make install

        $ make new-project

        # ex.
        #
        # project_name [프로젝트 이름]: nuj-project
        # description [프로젝트에 대해 간략하게 설명해주세요]: nuj' ml project for example
        # team [소속 팀을 적어주세요. (ex. AI 팀)]: data platform team
        # author [작성자]: nuj
        # email [이메일]: nuj@socar.kr

3. 프로젝트 초기화

    - 프로젝트를 생성하고나면 프로젝트 디렉토리가 생성
    - 프로젝트 디렉토리에 진입해 프로젝트를 초기화합니다.
  
            $ cd "프로젝트 이름"
            $ make init

            # ex.
            #
            # cd nuj-project
            # make init

4. 노트북에서 실험하기
    - 주피터 노트북(혹은 랩)에서 실험을 진행합니다.
    - 노트북 파일은 `notebooks/`에 담습니다.
    - 실험 기록은 `mlflow` 라이브러리를 활용하며, 예제는 `notebooks/example/`에서 확인합니다.


5. 배포를 위한 스크립트 파일(.py) 만들기
    - 배포를 위해 노트북 파일을 스크립트 파일로 변환합니다.

            $ make build file="노트북 파일 상대 경로"
            # ex. make build file=notebooks/example/pytorch.ipynb

    - `train.py` 가 만들어집니다.
    
            $ ls
            ...
            train.py

6. 프로젝트 저장소에 저장하기
    - 변경된 내용을 프로젝트 저장소인 Github Repo에 저장합니다.

            $ git add .
            $ git commit -m "example 프로젝트를 저장한다."
            $ git push origin <project name>


## ML프로젝트 실험하기

- ML 모델을 train & validation 하는 단계입니다.
- mlflow
    - 개발 환경 : http://mlflow.mlops.socar.me


### 환경변수 설정
- `MLFLOW_TRACKING_URI` : 배포된 mlflow url
- `GOOGLE_APPLICATION_CREDENTIALS` : GCP 서비스 계정 Credential

        export MLFLOW_TRACKING_URI="http://mlflow.mlops.socar.me"
        export GOOGLE_APPLICATION_CREDENTIALS={{서비스 계정(json)의 절대 경로}}

### Online 학습하기

        $ somlier online train PROJECT_NAME PROJET_REF --github_uri ${GITHUB_URI}
- Argument
    - `PROJECT_NAME (str)`
        - MLProjects 레포의 상대 경로입니다 (e.g, example-projects/sklearn)
    - `PROJECT_REF (str)`
        - MLProject 내 Git Ref 입니다 (e.g., 브랜치 이름, commit hash)
    
- Flag/Option
    - `--github_uri (str)`
        - github uri 를 지정합니다. (기본값 : [socar-data-ml-project](https://github.com/socar-inc/socar-data-ml-projects))


## Model 등록 및 테스트하기

- ML 모델을 등록 및 테스트하는 단계입니다.

### 실험한 모델 등록하기

- 실험한 모델 등록은 2가지 방법이 있습니다.
    - `somlier online register`를 이용한 방법
    - `mlflow dashboard`를 이용한 방법


**1. `somlier online register` 를 이용한 방법**

- 첫번째 인자에 등록할 실험의 `RUN_ID` 를 넣어줍니다.

    <p align="center">
      <img src="../images/mlflow_1.png" width="100%" />
    </p>


- 두번째 인자에 등록될 `모델의 이름`을 넣어줍니다.

         $ somlier online register 2f087c4eaec04b258e86e6fbed7d350b test_grab_model

         # Successfully registered model 'test_nuj_model'.
         # 2022/03/11 11:18:43 INFO mlflow.tracking._model_registry.client: Waiting up to 300 seconds for model version to finish creation.                     Model name: test_nuj_model, version 1
         # Created version '1' of model 'test_nuj_model'.
         # model version: 1

**2. `mlflow`에서 직접 등록하기

- 등록할 실험에서 `register model`을 클릭합니다
    <p align="center">
      <img src="../images/mlflow_2.png" width="100%" />
    </p>

- 등록할 모델 이름을 적고 등록된 모델을 확인합니다.
    <p align="center">
      <img src="../images/mlflow_3.png" width="100%" />
    </p>

    <p align="center">
      <img src="../images/mlflow_4.png" width="100%" />
    </p>




### ML Project 구조

- ML project 의 구조는 아래와 같으며, 대부분의 경우 1, 2, 3번을 수정해 배포하게 됩니다.

        ├── Dockerfile
        ├── MLproject
        ├── Makefile
        ├── README.md
        ├── __init__.py
        ├── entrypoint.sh
        ├── main.py # 3
        ├── notebooks
        ├── requirements.txt
        ├── service.py # 2
        ├── somlier.yaml # 1
        ├── test.py
        └── train.py



### Model 동작 테스트하기

- SoMLier Config 확인
      - 프로젝트에 사용된 config를 확인합니다. 

               $ somlier config show
         
               # 		  _____       __  _____    _
               #         / ___/____  /  |/  / /   (_)__  _____
               #         \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
               #        ___/ / /_/ / /  / / /___/ /  __/ /
               #       /____/\____/_/  /_/_____/_/\___/_/
               
               # SoMLier YAML: [/home/jovyan/socar-data-ml-projects/my-example-project /soda-project.yaml]
               # Model Name: my-example-project
               # Model Version: v0.0.1
               # Model Tag: ['dev']
               # Model Assets: []
               # Python Version: 3.8.7
               # Docker Image Name: my-example-project:['latest']
   

- SoMLier config Dependencies 확인
      - requirement.txt 에 정의된 dependencies 를 확인합니다.
               
               $ somlier config show -d
               #          _____       __  _____    _
               #         / ___/____  /  |/  / /   (_)__  _____
               #         \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
               #        ___/ / /_/ / /  / / /___/ /  __/ /
               #       /____/\____/_/  /_/_____/_/\___/_/
               
               # -------- dependencies --------
               # pandas=1.2.1
               # numpy=1.1.1
               # ------------------------------


- 모델 동작 테스트
      - `entrypoint.sh` 를 정의합니다.

               #!/bin/bash
               python main.py



      - `somlier.yaml`에서 entrypoints 속성 정의합니다.

               project:
                 docker:
                   env: []
                   name: nuj-test
                   tags:
                   - latest
                   volumes: []
                 name: nuj-test
                 python:
                   quirements_txt: requirements.txt
                   version: 3.8.7


         
               model:
                 assets: []
                 config: {}
                 name: nuj-test
                 tags:
                   - dev
                 version: v0.0.1
               
               t:
                 main:
                   command: bash
                   args: ["entrypoint.sh"]
                 test:
                   command: python
                   args: ["-m", "test"]
      

- 모델이 SoMLier 환경에서 정상적으로 실행되는지 확인합니다.


         $ somlier config run main

         #         _____       __  _____    _
         #        / ___/____  /  |/  / /   (_)__  _____
         #        \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
         #       ___/ / /_/ / /  / / /___/ /  __/ /
         #      /____/\____/_/  /_/_____/_/\___/_/
             
         # Entrypoint: [main] 을/를 실행합니다.
         # Executing ['python', 'main.py']...
         # {"name": "main", "stdout": "hello world!!\n", "timestamp": "2022-08-17T18:50:24.775569"}



## 모델 배포하기
- 배포에 사용될 이미지 생성 및 배포하는 단계입니다.

### Model Image 생성

- somlier config test 까지 완료됐다면, 배포에 사용될 이미지를 생성합니다.

                $ git add .
                $ git commit -m "feat(my-example-project): train.py 를 생성 후 수정한다"
                $ git push origin my-example-project 

- [socar-data-ml-project](https://github.com/socar-inc/socar-data-ml-projects) 에 올라간 브랜치(my-example-project) -> main 으로 PR 생성합니다.

<p align="center">
  <img src="../images/product_1.png" width="80%" />
</p>

- PR 생성되면 자동으로 해당 프로젝트의 도커 이미지가 생성됩니다.
- 도커 이미지 빌드가 완료되면, 슬랙 채널 `#dp_monitor_cicd`에 알림을 확인합니다.

<p align="center">
  <img src="../images/product_2.png" width="80%" />
</p>

- 해당 알림을 통해 build 된 이미지 이름을 확인합니다. <br> ex) `gcr.io/socar-date-dev/ml-my-example-project:latest`

### 모델 배포하기

- 모델이 포함된 이미지가 빌드됐다면, 개발 환경에서 직접 배포 테스트를 합니다.
- 모델 배포는 크게 2가지로 나뉩니다.
    - Offline(배치)
    - Online(실시간)

**1. OFFLINE (Airflow)** 

- offline 환경은 Airflow 를 활용해 사용자가 정의한 시간에 배치 작업(학습, 추론 등)이 수행됩니다.
- `somlier offline create`를 통해 Airflow 에서 동작할 Dag 파일을 생성합니다.

        $ somlier offline create "생성된 이미지" "스케줄할 시간(airflow interval)" "실행 커맨드" "생성될 dag id" ["템플릿 (e.g., default, mlops)"]["--gpu_type=nvidia-tesla-p100"] ["--num_of_gpus=GPU 갯수"]

ex) 매일 아침 9시에 인퍼런스하는 모델을 돌리고 싶은 경우

        $ somlier offline create \
          "gcr.io/socar-data-dev/ml-my-example-project:latest" \
          "0 9 * * *" \
          "run main" \ 
          "grab_tutorial"
        
        # grab_tutorial.py에 DAG가 생성되었습니다.
            
        $ ls -l

        # ...
        # -rw-r--r--  1 jovyan users   916 Mar  7 07:17 grab_tutorial.py
        

- 생성된 Dag python file을 확인합니다


        # $ cat grab_tutorial.py
        
        from datetime import datetime
        
        from airflow import models
        from operators import mlops_offline_operator as mlops
        
        from pendulum import timezone
        
        
        with models.DAG(
            dag_id="grab_tutorial",
            tags=['data-group'],
            description="",
            default_args={
                "owner": "data-group",
                "depends_on_past": False,
                "retries": 3,
            },
            start_date=datetime.strptime("2022-03-17 13:53:37.597257", "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone("Asia/Seoul")),
            schedule_interval="0 9 * * *",
            catchup=True,
            max_active_runs=1,
        ) as dag:
            t1 = mlops.MLOpsOfflineOperator(
                task_id="t1",
                ml_project_docker_image="gcr.io/socar-data-dev/ml-my-example-project:latest",
                project_name="grab_tutorial",
            )
    
- 생성된 Dag 를 업로드합니다.
    - [socar-data-mlops-dags](https://github.com/socar-inc/socar-data-mlops-dags) 레포에 PR을 만듭니다.
        - 생성한 브랜치 -> main 으로 머지되도록 PR 생성합니다.

    <p align="center">
      <img src="../images/product_3.png" width="80%" />
    </p>


- DAG 테스트 및 확인을 진행합니다.
    - [Airflow 개발 서버](https://airflow.mlops.socar.me/login/?next=https%3A%2F%2Fairflow.mlops.socar.me%2Fhome)에 접속합니다
    - `aws-dev-vpn`이 켜져있는지 확인합니다
        - username : admin
        - password : socar
    
    <p align="center">
      <img src="../images/product_4.png" width="80%" />
    </p>

    - 생성된 dag를 확인 후, Trigger Dag 로 돌립니다.

    <p align="center">
      <img src="../images/product_5.png" width="80%" />
    </p>
    
    <p align="center">
      <img src="../images/product_6.png" width="80%" />
    </p>

<br>

**2. Online (SoMLier - BentoML)** 

- cli 에 다음 커맨드를 입력해 온라인으로 배포를 합니다.
<br> `somlier online deploy MODEL_NAME MODEL_VERSION <flags>`

- Argument
    - `MODEL_NAME (str)`
    - `MODEL_VERSION (str)`
- Options
    - `--use_k8s (bool)`

- REST API 서버와 소통합니다.


        import requests
        import json
        
        url = "$SOMLIER_REST_API_URL/deploy"
        
        payload = json.dumps({
          "project_name": "YOUR_PROJECT_NAME",
          "model_name": "YOUR_MODEL_NAME",
          "model_version": "YOUR_MODEL_VERSION",
          "is_k8s": True | False,
          "istio_enabled": True | False,
          "use_gpu": True | False
        })
        headers = {
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
