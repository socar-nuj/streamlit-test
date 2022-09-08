
## SoMLier Train example
- SoMLier 를 이용해 노트북에서 모델 학습하는 방법을 익힙니다.
- 해당 예제는 Pytorch 모델을 기반으로 작성되었습니다.


### Import SomMLier and Packages
```angular2html
import torch
import torch.nn as nn
import torch.nn.functional as F
import somlier
```

- 노트북에서 `somlier` 및 필요한 package 를 import 합니다


### Set Experiment Name
```angular2html
# set experiment
somlier.set_experiment("nuj_somlier_test")
```

- `somlier.set_experiment(SET_EXPERIMENT)`에 원하는 Experiment 명을 입력합니다.
    - `SET_EXPERIMENT` : 저장할 Experiment 이름

<p align="center">
  <img src="../images/Experiment_1.png" width="30%" />
</p>


### Define Model and DataSet
```angular2html
# set data
X = torch.FloatTensor([[1], [2], [3]])
y = torch.FloatTensor([[2], [4], [6]])

# define model
model = nn.Linear(X.size()[-1], y.size()[-1])

# define parameters
lr = 0.01
nb_epochs = 2000

# define optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=lr)
```

- 데이터 및 모델을 정의합니다


### Train and Logging Model Data
```angular2html
# start mlflow run
with somlier.start_run():

    # log defined parameters
    somlier.log_param("lr", lr)
    somlier.log_param("nb_epochs", nb_epochs)

    # train model
    for epoch in range(nb_epochs+1):
        pred = model(X)
        cost = F.mse_loss(pred, y)
        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

    somlier.log_metrics
    # log trained model
    somlier.log_metrics({"mse": cost.item()})
    somlier.pytorch.log_model(pytorch_model=model, artifact_path="model")
```

- `with somlier.start_run()`을 통해 모델 학습을 진행합니다.

<p align="center">
  <img src="../images/Experiment_2.png" width="100%" />
</p>
- `User` 는 os.environ["LOGNAME"] 으로 자동 입력,  

- `somlier.log_param(PARAMETER_NAME, PARAMETER)`에 기록할 파라미터를 작성합니다.
    - `PARAMETER_NAME` : 기록할 파라미터 이름 정의
    - `PARAMETER` : 기록할 파라미터
- `somlier.log_metrics({"METRIC_NAME": METRIC})`에 기록할 메트릭을 "key":value 포멧으로 작성합니다.
    - `METRIC_NAME` : 기록할 메트릭 이름 정의
    - `METRIC` : 기록할 메트릭

<p align="center">
  <img src="../images/Experiment_3.png" width="70%" />
</p>

- `somlier.pytorch.log_model(PYTORCH_MODEL, ARTIFACT_PATH)` 에 위에서 학습한 모델과 저장할 위치를 정의합니다.
    - `PYTORCH_MODEL` : 위에서 학습한 모델
    - `ARTIFACT_PATH` : 학습한 모델의 artifact를 저장할 디렉토리 이름
- `pytorch` 이외의 모델은 `somlier.<MODEL_PACKAGE>.log_model` 을 이용합니다.
    - ex) `somlier.sklearn.log_model`