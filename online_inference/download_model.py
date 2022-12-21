# -*- coding: utf-8 -*-
from online_inference.entities.model_download_params import InferenceDownloadParams
from online_inference.downloader import download_file_from_google_drive
import os
from path import Path


def download_model(cfg: InferenceDownloadParams) -> None:
    # данные лежат на гугл диске.
    if not Path(cfg.model_path).exists():
        Path(cfg.model_path).makedirs()
    cfg.file_id = os.environ.get('MLOPS_HW2_MODEL_FILE_ID')
    download_file_from_google_drive(
        cfg.file_id, Path(cfg.model_path)/Path(cfg.model_name), cfg.url)


if __name__ == "__main__":
    os.environ['MLOPS_HW2_MODEL_FILE_ID'] = '1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC'
