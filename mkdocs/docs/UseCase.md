<p align="center">
  <img src="../images/soMLier_logo.png" width="300" />
</p>

<br>


## 유즈 케이스

<p align="center">
  <img src="../images/somlier_v2.png" width="100%" />
</p>

### 모델 개발

[ml-projects](https://github.com/socar-inc/socar-data-ml-projects) 레포에서 모델을 개발합니다

개발 방법은 [ml-projects의 README 문서](https://github.com/socar-inc/socar-data-ml-projects/blob/main/README.md) 를 확인해주세요

### 모델 트레이닝 (Train)

모델을 학습시킵니다

- CLI
    - Command

            $ somlier online train PROJECT_NAME PROJECT_REF --github_uri ${GITHUB_URI} {별도 주입이 필요한 경우 실험에 사용되는 parameter들의 조합}`

    - Parameter <br>
        - `PROJECT_NAME` - MLProjects 레포의 경로입니다 (e.g., example-projects/sklearn)
        - `PROEJCT_REF` - MLProjects 레포의 브랜치 또는 커밋 해시입니다 (e.g., main, a27738a)

    - Flag
        - `--github_uri` - 트레이닝 시킬 소스 코드의 깃헙 주소입니다 (e.g., git@github.com:socar-inc/socar-data-ml-projects.git)

    - 파라미터 조합별 병렬 학습 가이드
      
            $ somlier online train \
            PROJECT_NAME \
            PROJECT_REF \
            --github_uri ${GITHUB_URI} \
            --CONTINUOUS_PARAM_NAME START..END..INCREMENT \
            --DISCRETE_PARAM_NAME VALUE1,VALUE2,VALUE3,VALUE4 \
            --SINGLE_PARAM_NAME VALUE
          
        - 예시

                $ somlier online train \
                example-projects/torch-fashion-mnist \
                main \
                --github_uri git@github.com:socar-inc/socar-data-ml-projects.git \
                --learning_rate 0.001..0.005..0.001 \
                --batch_size 64,128 \
                --num_epochs 3
            
            - 위의 명령어를 실행하면
                - learning_rate = 0.001, 0.002, 0.003, 0.004 총 4가지
                - batch_size = 64, 128 총 2가지
                - num_epochs = 총 1가지
                - 3가지 파라미터에 대해 총 4 * 2 * 1 = 8가지 조합에 대해 학습을 병렬적으로 실행합니다.

- Web Server
    - Request
      
            # shell
            $ curl --location --request POST '${SOMLIER_WEBSERVER}/train' \
            --header 'Content-Type: application/json' \
            --data-raw '{
            "project_name": "PROJECT_NAME",
            "project_ref": "PROJECT_REF"
            }'

            # python
            import requests
            import json

            url = f"{SOMLIER_WEBSERVER}/train"

            payload = json.dumps({
              "project_name": f"{PROJECT_NAME}",
              "project_ref": f"{PROJECT_REF}"
            })
            headers = {
              'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)

    - Response
      
            {
              "run_id": "string",
              "status": "string"
            }
      

### 모델 검색 (Search)

레지스트리에 등록된 모델을 메트릭에 따라 쿼리합니다

- CLI
    - Command

      `$ somlier search PROJECT_NAME STANDARD_METRIC ORDER_BY`

    - Parameter

        - `PROJECT_NAME` - `train`에서 만든 프로젝트 이름입니다
        - `STANDARD_METRIC` - 기준 메트릭입니다 (e.g., `training_mae`)
        - `ORDER_BY` - 정렬 기준입니다 (e.g., `DESC`, `ASC`)

- Web Server
  - Request

          # shell
          $ curl --location --request POST '${SOMLIER_WEBSERVER}/search' \
          --header 'Content-Type: application/json' \
          --data-raw '{
              "project_name": "${PROJECT_NAME}",
              "standard_metric": "${STANDARD_METRIC}",
              "order_by": "${ORDER_BY}"
          }'

          # python
          import requests
          import json  

          url = f"{SOMLIER_WEBSERVER}/search"

          payload = json.dumps({
              "project_name": f"{PROJECT_NAME}",
              "standard_metric": f"{STANDARD_METRIC}",
              "order_by": f"{ORDER_BY}"
          })
          headers = {
            'Content-Type': 'application/json'
          }

          response = requests.request("POST", url, headers=headers, data=payload)

          print(response.text)
  
  - Response

          {
            "run_id": "string",
            "metric_value": "string"
          }
      

### 모델 레지스트리 등록 (Register)

모델을 레지스트리에 등록합니다

- CLI
    - Command

              $ somlier register RUN_ID MODEL_NAME

    - Parameter

        - `RUN_ID` - 모델 트레이닝 결과 id 값입니다. MLFlow 웹페이지에서 확인하시거나, `search`의 output을 확인해주세요
        - `MODEL_NAME` - 모델 이름입니다. 모델 레지스트리에서 해당 이름으로 모델이 등록됩니다

- Web Server
    - Request
          
              # shell
              $ curl --location --request POST '${SOMLIER_WEBSERVER}/register' \
              --header 'Content-Type: application/json' \
              --data-raw '{
                "run_id": "${RUN_ID}",
                "model_name": "${MODEL_NAME}"
              }'
    
              # python
              import requests
              import json
    
              url = f"{SOMLIER_WEBSERVER}/register"
    
              payload = json.dumps({
                "run_id": f"{RUN_ID}",
                "model_name": f"{MODEL_NAME}"
              })
              headers = {
                'Content-Type': 'application/json'
              }
    
              response = requests.request("POST", url, headers=headers, data=payload)
    
              print(response.text)

    - Response

            {
              "model_version": "string",
              "is_newer_version": bool,
              "message": "string"
            }

### 모델 레지스트리 등록 (Register_v2)

모델을 레지스트리에 등록합니다.

SoMLier를 통해 학습된 모델이 아니더라도 등록할 수 있습니다.

단, pytorch 모델 등록을 원할 경우 참조할 수 있는 모델 클래스 파일이 git에 업로드되어 있어야 합니다.

- CLI
    - Command

      `$ somlier online register_v2 MODEL_TYPE GCS_URI MODEL_NAME <flags>`

    - Parameter
        - `MODEL_TYPE` - 등록할 모델의 종류입니다. sklearn(scikit-learn), pytorch(torch) 타입을 제공하고 있습니다.
        - `GCS_URI` - 학습된 모델의 weights 파일이 저장된 GCS URI입니다. (gs://~)
        - `MODEL_NAME` - 모델 이름입니다. 모델 레지스트리에서 해당 이름으로 모델이 등록됩니다.

    - Flags
        - `GITHUB_URI` - (pytorch 모델을 로드할 경우) 모델 클래스 코드가 위치하는 github repository의 주소입니다. (e.g., git@github.com:socar-inc/socar-data-ml-projects.git)
        - `PROJECT_NAME` - (pytorch 모델을 로드할 경우) 모델 클래스 코드가 위치하는 프로젝트 이름입니다. (e.g., safe_driving_scoring)
        - `PROJECT_REF` - (pytorch 모델을 로드할 경우) 모델 클래스 코드가 위치하는 브랜치 이름입니다. (e.g, main)
        - `MODEL_MODULE_PATH` - (pytorch 모델을 로드할 경우) 모델 클래스 코드가 위치하는 경로입니다. (e.g, models/lstm_classifier.py)
        - `MODEL_CLASS_NAME` - (pytorch 모델을 로드할 경우) 모델 클래스 이름입니다. (e.g, LSTMEnsembleReservationClassifier)

    - Example

            $ somlier online register_v2 \
            pytorch \
            gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth \
            sts-drgps-acceleration-accident-risk \
            git@github.com:socar-inc/socar-data-ml-projects.git \
            safe_driving_scoring \
            main \
            models/lstm_classifier.py \
            LSTMEnsembleReservationClassifier


### 모델 동작 테스트 (Config)
SoMLier 환경에서 모델 동작을 테스트합니다

1. `entrypint.sh` 및 `somlier.yaml` 을 정의합니다
   

       - Example <br>

               #!/bin/bash
                            
               python main.py
            
    
          `somlier.yaml`
    
            ...
    
            project:
              docker:
                env: []
                name: nuj-test
                tags:
                - latest
                volumes: []
              name: nuj-test
              python:
                requirements_txt: requirements.txt
                version: 3.8.7
    
            model:
              assets: []
              config: {}
              name: nuj-test
              tags:
                - dev
              version: v0.0.1
    
            entrypoint:
              main:
                command: bash
                args: ["entrypoint.sh"]
              test:
                command: python
                args: ["-m", "test"]



2. config 및 dependencies 를 확인합니다

     - CLI
   
        - Command <br>
                `$ somlier config show [-d, --dependencies]`

        - Flag

              - `dependencies` - requirements.txt 내 Dependencies 확인 여부입니다. <br> (e.g., default=False)

        - Example

                 $ somlier config show
    
                 #		   _____       __  _____    _
                 #        / ___/____  /  |/  / /   (_)__  _____
                 #        \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
                 #       ___/ / /_/ / /  / / /___/ /  __/ /
                 #      /____/\____/_/  /_/_____/_/\___/_/
    
                 # SoMLier YAML: [/home/jovyan/socar-data-ml-projects/my-example-project /soda-project.yaml]
                 # Model Name: my-example-project
                 # Model Version: v0.0.1
                 # Model Tag: ['dev']
                 # Model Assets: []
                 # Python Version: 3.8.7
                 # Docker Image Name: my-example-project:['latest']
<br>
    
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


3. SoMLier 환경에서 모델 동작을 확인합니다

     - CLI
         - Command
           `$ somlier config run ENTRYPOINT`

         - Parameter
             - `ENTRYPOINT` - `somlier.yaml` 에서 정의한 entrypoint 입니다.

         - Example
          

                   $ somlier config run main
            
                   #         _____       __  _____    _
                   #        / ___/____  /  |/  / /   (_)__  _____
                   #        \__ \/ __ \/ /|_/ / /   / / _ \/ ___/
                   #       ___/ / /_/ / /  / / /___/ /  __/ /
                   #      /____/\____/_/  /_/_____/_/\___/_/
            
                   # Entrypoint: [main] 을/를 실행합니다.
                   # Executing ['python', 'main.py']...
                   # {"name": "main", "stdout": "hello world!!\n", "timestamp": "2022-08-17T18:50:24.775569"}
             

### 모델 서빙 (Deploy)

모델을 배포합니다

- CLI
    - Command

      `$ somlier deploy PROJECT_NAME MODEL_NAME MODEL_VERSION [--use_k8s_job=bool] [--istio_enabled=bool]`

    - Parameter

        - `PROJECT_NAME` - `train`에서 만든 프로젝트 이름입니다
        - `MODEL_NAME` - `register`에서 모델 레지스트리에 등록한 모델 이름입니다
        - `MODEL_VERSION` - 모델의 버전입니다. MLFlow에서 자동으로 갱신됩니다. (e.g., "1", "2")
  
    - Flag
        - `--use_k8s_job` - 모델을 쿠버네티스 상에 배포할 지에 대한 여부입니다 (e.g., default=True)
        - `--istio_enabled` - 쿠버네티스 상에 istio가 적용되어있는 지 여부 입니다 (e.g., default=False)

- Web Server
    - Request

              
            # shell
            $ curl --location --request POST '${SOMLIER_WEBSERVER}/deploy' \
            --header 'Content-Type: application/json' \
            --data-raw '{
              "project_name": "${PROJECT_NAME}",
              "model_name": "${MODEL_NAME}",
              "model_version": "${MODEL_VERSION}",
              "use_k8s_job": ${use_k8s_job},
              "istio_enabled": ${istio_enabled}
            }'
    
            # python
            import requests
            import json
    
            url = f"{SOMLIER_WEBSERVER}/deploy"
    
            payload = json.dumps({
              "project_name": "${PROJECT_NAME}",
              "model_name": "${MODEL_NAME}",
              "model_version": "${MODEL_VERSION}",
              "use_k8s_job": ${use_k8s_job},
              "istio_enabled": ${istio_enabled}
            })
            headers = {
              'Content-Type': 'application/json'
            }
    
            response = requests.request("POST", url, headers=headers, data=payload)
    
            print(response.text)


    - Response

            {
              "status": "string",
              "message": "string"
            }


### 배치/오프라인 모델 서빙 (batch)

Batch 서빙을 위해 Airflow DAG를 만들고, 배포합니다

- CLI
    - Command
      
        `$ somlier batch SUBCOMMAND DOCKER_IMAGE SCHEDULE ENTRYPOINT DAG_ID <flags>`

    - Parameter
        - `subcommand`: 서브 커멘드 (e.g., create)
        - `docker_image`: 도커 이미지 (e.g., gcr.io/socar-data-dev/sift:latest)
        - `schedule`: Airflow schedule expression (e.g., 0 0 * * *)
        - `entrypoint`: 컨테이너의 entrypoint (e.g., sh -c predict.sh, make predict)
        - `dag_id` : DAG id (주의: unique 해야합니다)
    - Flag
        - `dry_run`: dry run 여부 (False - git push 하지 않습니다)
        - `check_airflow`: airflow 체크 여부 (False - Airflow REST API로 DAG가 정상적으로 마운트 됐는지 확인합니다)


- Web Server
  **아직 구현되지 않았습니다**



### 배치/오프라인 모델 서빙 (offline register_v2)

Batch 서빙을 위해 Airflow DAG을 만들고, 배포합니다.

위의 usecase와의 차이점은 별도의 도커 이미지 없이도 MLOps Offline Operator를 이용해 DAG 제작이 가능합니다.

현재까지는 일 단위 배포를 지원합니다. 시간 단위 또는 custom한 주기 지원은 추후 추가될 예정입니다.

- CLI
    - Command
  
        `$ somlier offline create_v2 MODEL_REF DAG_ID SCHEDULE_INTERVAL DATASET_REF DATASET_LOAD_COLUMN DESTINATION_TABLE_REF GITHUB_PERSONAL_ACCESS_TOKEN <flags>`

    - Paramater
        - `MODEL_REF` : MLflow Model Registry에 저장된 모델 ref (e.g., boston-house-pricing/2)
        - `DAG_ID` : DAG ID (주의: unique 해야 합니다.)
        - `SCHEDULE_INTERVAL` : Airflow schedule expression (e.g., 0 0 * * *)
        - `DATASET_REF` : 머신러닝 모델이 참조할 feature dataset table (주의: Bigquery에 존재해야 합니다.) (e.g., temp_serena.boston_house_pricing_feature_set)
        - `DATASET_LOAD_COLUMN` : feature dataset table에서 인퍼런스 대상을 조회할 기준이 될 컬럼 (e.g., date, return_date_kst)
        - `DESTINATION_TABLE_REF` : 머신러닝 모델의 인퍼런스 결과가 저장될 table (e.g., temp_serena.boston_house_pricing_result)
        - `GITHUB_PERSONAL_ACCESS_TOKEN` : socar-data-mlops-dags repository에 PR을 생성하기 위해 필요한 github personal access token입니다.
    - Flags
        - `START_DATE` : DAG의 시작 일자입니다. (default: command 실행 기준 1일 전)
        - `DATASET_LOAD_WINDOW` : 인퍼런스 대상을 선정할 기준 window입니다. `DATASET_LOAD_COLUMN`이 (DAG이 작동하는 일자 - DATASET_LOAD_WINDOW 일)에 해당하는 데이터를 인퍼런스합니다.
            - (default: 1 --> 일반적으로 하루 이전의 데이터에 대해 인퍼런스 할 경우, default 값을 사용합니다.)
        - `DATASET_LOAD_BY_KST` : `DATASET_LOAD_COLUMN`의 표준 시간대가 KST에 해당하는지 여부입니다.
            - (default: True)

    - Example

            $ somlier offline create_v2 \
            boston-house-pricing/2 \
            inference_boston_house_price \
            "0 9 * * *" \
            temp_serena.boston_house_pricing_feature_set \
            date \
            temp_serena.boston_house_pricing_result \
            GITHUB_PERSONAL_ACCESS_TOKEN


- Web Server
  **아직 구현되지 않았습니다**
