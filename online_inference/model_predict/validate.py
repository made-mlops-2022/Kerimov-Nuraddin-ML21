import pandas as pd
from path import Path
from typing import List
from online_inference.entities.validate_params import ValidateParams
from sklearn.ensemble import IsolationForest
from online_inference.downloader import download_file_from_google_drive
from ml_example.data.make_dataset import read_data
import zipfile


def load_train_data(cfg: ValidateParams):

    # данные лежат на гугл диске. Или брать тут kaggle datasets download -d cherngs/heart-disease-cleveland-uci
    # '1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4'
    if not (Path(cfg.data_path)/Path(cfg.data_name)).exists():
        if not Path(cfg.data_path).exists():
            Path(cfg.data_path).makedirs()
        download_file_from_google_drive(
            cfg.file_id, f'{cfg.data_path}/{cfg.zip_path}', cfg.url)
        with zipfile.ZipFile(f'{cfg.data_path}/{cfg.zip_path}', 'r') as zip_ref:
            zip_ref.extractall(cfg.data_path)

    global train_data, min_data, max_data, isol_forest
    train_data = read_data(f'{cfg.data_path}/{cfg.data_name}')
    max_data = train_data.drop(columns=['condition']).max()
    min_data = train_data.drop(columns=['condition']).min()
    isol_forest = IsolationForest(n_estimators=1000, contamination=0.001)
    isol_forest.fit(train_data.drop(columns=['condition']))


def validate(data: pd.DataFrame):
    """
    separates valid data from non valid. 
    non valid data is marked with condition = -1
    Args:
        data:pd.Dataframe - input data
    Returns
        valid_data: pd.Dataframe - validade
    """
    data_columns = data.columns
    correct_order_columns = ['name', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                             'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'condition']

    if (data_columns == correct_order_columns).all():

        valid_mask = (data.drop(columns=['name', 'condition']) >= min_data) & (
            data.drop(columns=['name', 'condition']) <= max_data)

        data['isol_forest'] = isol_forest.predict(
            data.drop(columns=['name', 'condition']))
        valid_data = data[valid_mask.all(axis=1)]

        non_valid_data = pd.concat(
            [valid_data[valid_data['isol_forest'] == -1], data[(~valid_mask).any(axis=1)]])
        non_valid_data['condition'] = -1

        valid_data = valid_data[valid_data['isol_forest'] == 1]

        return (valid_data.drop(columns='isol_forest'), non_valid_data.drop(columns='isol_forest'))

    data['condition'] = -1
    return None, data
