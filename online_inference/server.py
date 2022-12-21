from typing import List
from path import Path
from fastapi import FastAPI, Response
import pandas as pd
import hydra
import pickle
import os
import sys
import time
from hydra.core.config_store import ConfigStore
from online_inference.entities.input_data import InputData
from online_inference.entities.inference_params import InferenceParams
from online_inference.download_model import download_model
from online_inference.model_predict.predict import predict
from online_inference.model_predict.validate import validate, load_train_data
ins = ConfigStore.instance()

ins.store(name="conf", node=InferenceParams)


app = FastAPI()


model_ready = False
to_die=False

@app.on_event("startup")
def startup_model():
    with hydra.initialize(version_base=None, config_path="../configs", job_name="test_app"):
        cfg = hydra.compose(config_name='inference_config')
    if cfg.need_download_model or not Path(f'{cfg.download_params.model_path}/{cfg.download_params.model_name}').exists():
        download_model(cfg.download_params)
    global model, model_ready
    # raise BaseException(f'{cfg.download_params.model_path}/{cfg.download_params.model_name}')

    with open(f'{cfg.download_params.model_path}/{cfg.download_params.model_name}', 'rb') as f:
        model = pickle.load(f)
    load_train_data(cfg.train_data_params)
    time.sleep(20)
    model_ready = True


@app.get("/")
def default():
    return {"Name": "HW2",
            'Author': 'Kerimov Nuraddin'}


@app.post("/predict")
def predict_entrypoint(inp_data: List[InputData], response: Response):
    """
        validate and predict data

        Args:
            inp_data:InputData List of cases

        Returns:
            List[InputData]: List of cases with condition column
    """
    response.status_code = 400
    data = pd.DataFrame(list(map(dict, inp_data)))
    if model_ready:
        valid_data, non_valid_data = validate(data)
        if valid_data is not None and valid_data.shape[0] > 0:
            valid_data = predict(model, valid_data)
            response.status_code = 200
            return pd.concat([valid_data, non_valid_data]).to_dict('records')
        return "No valid data"
    return 'model isnt ready'


@app.get("/health")
def health(response: Response):
    if (to_die):
        if time.time() - start_time > 60:
            sys.exit()
    response.status_code = 200 if model_ready else 503
    to_die = True
    start_time = time.time()
    return model_ready
    

