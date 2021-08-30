import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from get_data import read_params
import argparse
import joblib
import json
import logging

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s', level=logging.INFO, filename='Training_logs/training_and_evaluation.log', filemode='w')

def eval_metrics(actual, pred):
    """
        process evaluation metrics
    """
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    """
        split the data and save it
    """
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_data"]
    train_data_path = config["split_data"]["train_data"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]
    webapp_model_dir = config["webapp_model_dir"]

    bootstrap = config["estimators"]["RandomForestRegressor"]["params"]["bootstrap"]
    max_depth = config["estimators"]["RandomForestRegressor"]["params"]["max_depth"]
    max_features = config["estimators"]["RandomForestRegressor"]["params"]["max_features"]
    min_samples_leaf = config["estimators"]["RandomForestRegressor"]["params"]["min_samples_leaf"]
    min_samples_split = config["estimators"]["RandomForestRegressor"]["params"]["min_samples_split"]
    n_estimators = config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
    target = [config["base"]["target_col"]]

    logging.info("Loading the train and test data")
    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train.loc[:,target]
    test_y = test.loc[:,target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    logging.info("Starting training")
    lr = RandomForestRegressor(bootstrap=bootstrap,
                               random_state=random_state,
                               max_depth=max_depth,
                               max_features=max_features,
                               min_samples_leaf=min_samples_leaf,
                               min_samples_split=min_samples_split,
                               n_estimators=n_estimators)
    lr.fit(train_x, train_y.values.ravel())

    predicted_qualities = lr.predict(test_x)
    lr.score(test_x, test_y)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
    logging.info("Training complete, got RMSE: %s, MAE: %s ,R2: %s" % (rmse, mae, r2))

    print("Got RMSE:%s, MAE:%s ,R2:%s" % (rmse, mae, r2))

    #####################################################
    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
            "bootstrap" : bootstrap,
            "max_depth" : max_depth,
            "max_features" : max_features,
            "min_samples_leaf" : min_samples_leaf,
            "min_samples_split" : min_samples_split,
            "n_estimators" : n_estimators}
        json.dump(params, f, indent=4)

    #####################################################

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(lr, model_path)
    joblib.dump(lr, webapp_model_dir)
<<<<<<< HEAD
    logging.info("Saved models!")
=======
>>>>>>> af452be... data



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
