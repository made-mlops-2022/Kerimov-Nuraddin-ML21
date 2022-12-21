from sklearn.pipeline import Pipeline
import pandas as pd


def predict(model: Pipeline, data: pd.DataFrame) -> pd.DataFrame:
    """
    launching prediction pipeline

    Args:
        model: Pipeline - input model with .predict() method
        data: pd.DataFrame - data to predict
    Returns:
        pd.Dataframe - data with predicted values

    """
    predicts = model.predict(data.drop(columns=['name', 'condition']))
    data['condition'] = predicts
    return data
