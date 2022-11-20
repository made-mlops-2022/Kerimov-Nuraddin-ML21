import pickle
from typing import Dict, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from ml_example.enities.train_params import TrainingParams
from catboost import Pool
from catboost import CatBoostClassifier



def train_model(
    features: pd.DataFrame, target: pd.Series,val_features:pd.DataFrame, val_target: pd.Series, train_params: TrainingParams):
    if train_params.model_type == "CatBoostClassifier":
        
        model = CatBoostClassifier(
        iterations=train_params.iterations,
        random_seed=train_params.random_seed,
        learning_rate=train_params.learning_rate,
        custom_loss=train_params.custom_loss,
        use_best_model=train_params.use_best_model
        )

        model.fit(
            features, target,
            cat_features=train_params.cat_features,
            eval_set=(val_features, val_target),
            verbose=True,
        )
    elif train_params.model_type == 'LogisticRegression':
        model = LogisticRegression()
        model.fit(
            features, target
        )
    else:
        raise NotImplementedError()
    return model


def predict_model(
    model: Pipeline, features: pd.DataFrame
) -> np.ndarray:
    predicts = model.predict(features)
    return predicts


def evaluate_model(
    predicts: np.ndarray, target: pd.Series
) -> Dict[str, float]:
    pr, rec, f1,_ =precision_recall_fscore_support(target,predicts,average= 'binary')
    return {
        "precision": pr,
        "recall": rec,
        "f1": f1
    }


def create_inference_pipeline(
    model, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([("feature_part", transformer), ("model_part", model)])


def serialize_model(model: object, output: str) -> str:
    with open(output, "wb") as f:
        pickle.dump(model, f)
    return output

def load_model(model_path:str) -> Pipeline:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model
