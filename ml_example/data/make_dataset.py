# -*- coding: utf-8 -*-
from typing import Tuple
import requests as r
from sklearn.model_selection import train_test_split
from ml_example.enities.download_params import DownloadParams
from ml_example.enities.split_params import SplittingParams
import zipfile
import pandas as pd
import numpy as np
import sys
import os
# https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url


def download_file_from_google_drive(file_id: str, destination: str, url: str) -> None:
    session = r.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    print(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)
    # session.close()


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination: str) -> None:
    CHUNK_SIZE = 32768  # hardcode

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_data(cfg: DownloadParams) -> None:
    # данные лежат на гугл диске. Или брать тут kaggle datasets download -d cherngs/heart-disease-cleveland-uci
    # '1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4'
    if not os.path.exists(cfg.path):
        os.makedirs(cfg.path)
    download_file_from_google_drive(
        cfg.file_id, cfg.path+'/'+cfg.zip_path, cfg.url)
    with zipfile.ZipFile(cfg.path+'/'+cfg.zip_path, 'r') as zip_ref:
        zip_ref.extractall(cfg.path+'/')


def read_data(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)


def split_train_val_data(
    data: pd.DataFrame, params: SplittingParams
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_data, val_data = train_test_split(
        data, test_size=params.val_size, random_state=params.random_state
    )
    return train_data, val_data


def save_predicted_results(data: pd.DataFrame, predicts: np.array, output_path: str) -> None:
    data['predicted'] = predicts
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    data.to_csv(output_path, index=False)


def generete_fake_data(path, samples) -> None:
    data = pd.DataFrame()
    data['age'] = np.random.normal(loc=58, scale=30, size=samples).astype(int)
    data['sex'] = np.random.randint(0, 1, size=samples)
    data['cp'] = np.random.randint(0, 3, size=samples)
    data['trestbps'] = np.random.normal(
        loc=130, scale=20, size=samples).astype(int)
    data['chol'] = np.random.normal(
        loc=250, scale=100, size=samples).astype(int)
    data['fbs'] = np.random.randint(0, 1, size=samples)
    data['restecg'] = np.random.randint(0, 2, size=samples)
    data['thalach'] = np.random.normal(
        loc=160, scale=60, size=samples).astype(int)
    data['exang'] = np.random.randint(0, 1, size=samples)
    data['oldpeak'] = np.abs(np.random.normal(
        loc=0, scale=3, size=samples).astype(int))
    data['slope'] = np.random.randint(0, 2, size=samples)
    data['ca'] = np.random.randint(0, 3, size=samples)
    data['thal'] = np.random.randint(0, 2, size=samples)
    data['condition'] = np.random.randint(0, 1, size=samples)
    if not os.path.exists(path):
        os.makedirs(path)
    data.to_csv(path, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("need 2 params")
        sys.exit()

    generete_fake_data(sys.argv[1], int(sys.argv[2]))
