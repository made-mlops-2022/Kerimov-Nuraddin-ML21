from dataclasses import dataclass
from online_inference.entities.model_download_params import InferenceDownloadParams
from online_inference.entities.validate_params import ValidateParams


@dataclass
class InferenceParams:
    train_data_params: ValidateParams
    download_params: InferenceDownloadParams
    need_download_model: bool = True
