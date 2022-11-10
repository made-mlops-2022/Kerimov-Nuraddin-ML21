# -*- coding: utf-8 -*-
from typing import Tuple, NoReturn
import requests as r
import pandas as pd
from sklearn.model_selection import train_test_split
from ml_example.enities import SplittingParams
import hydra
from data_download_data_conf import Data_download
#https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
def download_file_from_google_drive(file_id:str, destination:str,url:str)->None:
    session = r.Session()

    response = session.get(url, params = { 'id' : file_id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(url, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination:str)->None:
    CHUNK_SIZE = 32768#hardcode

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

@hydra.main(config_path="config", config_name="train_config")
def download_data(cfg:Data_download):
    if  not cfg.path.exists(): # создаем папку, где будем хранить данные, если их вдруг нет
        cfg.path.mkdir()

    #данные лежат на гугл диске. Или брать тут kaggle datasets download -d cherngs/heart-disease-cleveland-uci
    if not cfg.csv.exists(): # если нет данных
        download_file_from_google_drive(cfg.file_id,cfg.zip_path,cfg.url)#'1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4',dirs['data_zip'])#качаем
        with zipfile.ZipFile(cfg.zip_path, 'r') as zip_ref:
            zip_ref.extractall(str(cfg.csv))

def split_train_val_data(
    data: pd.DataFrame, params: SplittingParams
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """

    :rtype: object
    """
    train_data, val_data = train_test_split(
        data, test_size=params.val_size, random_state=params.random_state
    )
    return train_data, val_data
