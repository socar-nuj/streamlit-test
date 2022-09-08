import somlier.application.use_cases.notebook.train

__version__ = "0.6.2"

cli_name = "somlier"

# mlflow to somlier in notebook
set_experiment = somlier.application.use_cases.notebook.train.set_experiment
start_run = somlier.application.use_cases.notebook.train.start_run
log_param = somlier.application.use_cases.notebook.train.log_param
log_metrics = somlier.application.use_cases.notebook.train.log_metrics
pytorch = somlier.application.use_cases.notebook.train.pytorch