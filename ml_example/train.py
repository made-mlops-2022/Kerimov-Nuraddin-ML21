import logging
import os
import json
import sys
from ml_example.data.make_dataset import download_data, split_train_val_data, read_data
from ml_example.enities.train_pipeline_params import TrainingPipelineParams

from ml_example.features import make_features
from ml_example.features.build_features import extract_target, build_transformer
from ml_example.models import (
    train_model,
    serialize_model,
    predict_model,
    evaluate_model,
)
import mlflow

from ml_example.models.model_fit_predict import create_inference_pipeline
import hydra
from hydra.core.config_store import ConfigStore

ins = ConfigStore.instance()

ins.store(name="conf", node=TrainingPipelineParams)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
conf_file_name = 'train_config'  # изменяется в main от консольного параметра!!


@hydra.main(version_base=None, config_path="../configs", config_name='train_config_catboost',)
def main(config: TrainingPipelineParams):
    if config.use_mlflow:
        mlflow.set_tracking_uri(config.mlflow_uri)
        mlflow.set_experiment(config.mlflow_experiment)
        with mlflow.start_run():
            mlflow.log_artifact('./outputs')
            model_path, metrics = train(config)
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(model_path)
    else:
        return train(config)


def train(config: TrainingPipelineParams) -> None:
    logger.info("Starting pipeline")
    logger.info(f"configs: {config}")
    input_data_path = config.input_data_path
    if config.download_data or (not os.path.exists(input_data_path)):
        logger.info(f"need to download data, ignoring input_data_params")
        logger.info(f"data already exists: {os.path.exists(input_data_path)}")
        download_data(config.downloading_params)
        input_data_path = config.downloading_params.path+'/'+config.downloading_params.csv

    logger.info(f"Start reading data")
    data = read_data(input_data_path)
    logger.info(f"data readed succesfully")
    logger.info(f"data.shape is {data.shape}")

    logger.info(f"splitting data to train and val")
    train_df, val_df = split_train_val_data(
        data, config.splitting_params
    )

    logger.info(
        f"train has {train_df.shape[0]} objects, val has {val_df.shape[0]} objects")

    logger.info(f"extracting and dropping target")
    val_target = extract_target(val_df, config.feature_params)
    train_target = extract_target(train_df, config.feature_params)
    train_df = train_df.drop(config.feature_params.target_col, 1)
    val_df = val_df.drop(config.feature_params.target_col, 1)

    logger.info(f"train_df.shape is {train_df.shape}")
    logger.info(f"val_df.shape is {val_df.shape}")

    logger.info(f"building transformers")
    transformer = build_transformer(config.feature_params)
    transformer.fit(train_df)
    train_features = make_features(transformer, train_df)

    transformer = build_transformer(config.feature_params)
    transformer.fit(val_df)
    val_features = make_features(transformer, val_df)
    logger.info(f"builded transformers succesfully")

    logger.info(f"start training {config.train_params.model_type}")
    model = train_model(
        train_features, train_target, val_features, val_target, config.train_params)
    logger.info(f"finished training")

    inference_pipeline = create_inference_pipeline(model, transformer)
    predicts = predict_model(
        inference_pipeline,
        val_df,
    )
    metrics = evaluate_model(
        predicts,
        val_target,
    )
    with open(config.metric_path, "w") as metric_file:
        json.dump(metrics, metric_file)
    logger.info(f"metrics is {metrics}")

    path_to_model = serialize_model(
        inference_pipeline, config.output_model_path
    )
    return path_to_model, metrics


if __name__ == "__main__":
    main()
