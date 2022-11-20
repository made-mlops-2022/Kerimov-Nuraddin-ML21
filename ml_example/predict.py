import logging
import os
import sys
from pathlib import Path
import json
import sys
import pandas as pd
from ml_example.data.make_dataset import read_data, save_predicted_results
from ml_example.models import  load_model, predict_model


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def predict(data_path:str, model_path:str, output_path:str)->None:
    logger.info("Starting predict")
    logger.info(f"data_path: {data_path}")
    logger.info(f"output_path: {output_path}")

    if not os.path.exists(data_path) or not os.path.exists(model_path):
        logger.error(f"INPUT FILE NOT FOUND")
        raise FileNotFoundError



    logger.info(f"Start reading data")
    data = read_data(data_path)
    logger.info(f"data readed succesfully")
    logger.info(f"data.shape is {data.shape}")

    

    logger.info(f"Start loading model")
    model = load_model(model_path)
    logger.info(f"Model loaded succesfully")

    
    predicts = predict_model(
        model,
        data,
    )
    
    logger.info(f"predicted successfully")

    save_predicted_results(data,predicts,output_path)
    



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("need 3 params")
        sys.exit()

    predict(sys.argv[1],sys.argv[2],sys.argv[3])