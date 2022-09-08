import mlflow

try:
    # pylint: disable=unused-import
    import mlflow.catboost as catboost
    import mlflow.fastai as fastai
    import mlflow.gluon as gluon
    import mlflow.h2o as h2o
    import mlflow.keras as keras
    import mlflow.lightgbm as lightgbm
    import mlflow.mleap as mleap
    import mlflow.onnx as onnx
    import mlflow.pyfunc as pyfunc
    import mlflow.pytorch as pytorch
    import mlflow.sklearn as sklearn
    import mlflow.spacy as spacy
    import mlflow.spark as spark
    import mlflow.statsmodels as statsmodels
    import mlflow.tensorflow as tensorflow
    import mlflow.xgboost as xgboost
    import mlflow.shap as shap
    import mlflow.pyspark as pyspark
    import mlflow.paddle as paddle
    import mlflow.prophet as prophet
    import mlflow.pmdarima as pmdarima
    import mlflow.diviner as diviner

    _model_flavors_supported = [
        "catboost",
        "fastai",
        "gluon",
        "h2o",
        "keras",
        "lightgbm",
        "mleap",
        "onnx",
        "pyfunc",
        "pytorch",
        "sklearn",
        "spacy",
        "spark",
        "statsmodels",
        "tensorflow",
        "xgboost",
        "shap",
        "paddle",
        "prophet",
        "pmdarima",
        "diviner",
    ]
except ImportError as e:
    # We are conditional loading these commands since the skinny client does
    # not support them due to the pandas and numpy dependencies of MLflow Models
    pass


set_experiment = mlflow.tracking.fluent.set_experiment
start_run = mlflow.tracking.fluent.start_run
log_param = mlflow.tracking.fluent.log_param
log_metrics = mlflow.tracking.fluent.log_metrics
pytorch = mlflow.pytorch
