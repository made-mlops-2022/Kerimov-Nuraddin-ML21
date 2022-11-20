from typing import Optional

from dataclasses import dataclass

from ml_example.enities.download_params import DownloadParams
from ml_example.enities.split_params import SplittingParams
from ml_example.enities.feature_params import FeatureParams
from ml_example.enities.train_params import TrainingParams


@dataclass()
class TrainingPipelineParams:
    input_data_path: str
    output_model_path: str
    metric_path: str
    splitting_params: SplittingParams
    feature_params: FeatureParams
    train_params: TrainingParams
    downloading_params: DownloadParams 
    download_data: bool = True
    use_mlflow: bool = False
    mlflow_uri: str = "http://18.156.5.226/"
    mlflow_experiment: str = "inference_demo"
    

