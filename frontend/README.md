# SoMLier Web Admin

---
### Train Model
- 기본 화면 구성
![img.png](images/train_default.png)

- 사용 방법 (Parameter 입력하지 않는 경우)
![img_2.png](images/train_usecase_without_parameters.png)

- 사용 방법 (Parameter 입력하는 경우)
![img.png](images/train_usecase_with_parameters_1.png)
![img.png](images/train_usecase_with_parameters_2.png)
![img.png](images/train_usecase_with_parameters_3.png)
![img.png](images/train_usecase_with_parameters_4.png)


---
### Register Model
- 기본 화면 구성
![img.png](images/register_default.png)

- 사용 방법
  - MLflow을 통해 학습된 모델의 경우
    ![img.png](images/register_usecase_with_mlflow_run.png)
  - 기존에 학습된 모델의 경우
    - sklearn 모델 
      ![img.png](images/register_usecase_with_sklearn.png)
    - torch 모델
      ![img.png](images/register_usecase_with_torch.png)
  

---
### Search Model
- 기본 화면
  ![img.png](images/search_default.png)
- 사용 방법
  ![img.png](images/search_usecase.png)


---
### Deploy Model
- WIP


---
### Offline Serve Model
- 기본 화면
  ![img.png](images/offline_serve_default.png)
- 사용 방법 
  - Docker Image를 이용한 경우 
    ![img.png](images/offline_serve_usecase_docker_1.png)
    - Download 버튼을 누르면 아래와 같은 스크립트 파일이 다운된다.
      ![img.png](images/offline_serve_usecase_docker_2.png)
  - SOCAR Data Provider를 이용한 경우
    ![img.png](images/offline_serve_usecase_provider.png)

