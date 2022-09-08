import torch
import torch.nn as nn
import torch.nn.functional as F
import somlier


# set experiment
somlier.set_experiment("nuj_somlier_test")

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