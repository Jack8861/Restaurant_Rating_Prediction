import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_params
import logging

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s', level=logging.INFO, filename='Training_logs/splitting_data.log', filemode='w')

def split_and_saved_data(config_path):
    """
        split the data into train and test data and save it
    """
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_data"]
    train_data_path = config["split_data"]["train_data"]
    processed_data_path = config["processed_data"]["processed_dataset_csv"]
    split_ratio = config["split_data"]["test_size"]
    random_state = config["base"]["random_state"]

    df = pd.read_csv(processed_data_path, sep=",", encoding='utf-8')
    logging.info("Splitting data into train and test sets")
    train, test = train_test_split(
        df,
        test_size=split_ratio,
        random_state=random_state
    )
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")
    logging.info("Data split successful")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)
