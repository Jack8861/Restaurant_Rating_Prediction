import pandas as pd
import numpy as np
from get_data import read_params
import re
import argparse
import logging

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s', level=logging.INFO, filename='Training_logs/preprocess_data.log', filemode='w')


def clean_rating(row):  # get the numeric values
    exp = re.compile('[0-9]\.[0-9]')
    rate = re.match(exp, row['rate'])[0]
    return rate


def get_ratings(df):
    try:
        # replace null values
        df[['rate']] = df[['rate']].replace({"NEW": '0.0', "-": '0.0', "nan": '0.0', np.NaN: '0.0'})
        # extract the rating
        df.rate = df.apply(clean_rating, axis=1)
        df.rate = df.rate.astype('float')
        # get the max rating of each restaurant
        rate = pd.DataFrame(df.groupby(['address'])['rate'].max())
    except Exception as e:
        logging.error("An error while getting ratings: %s" % e)
        raise
    return rate


def get_votes(df):
    try:
        votes = pd.DataFrame(df.groupby(['address'])['votes'].max())
    except Exception as e:
        logging.error("An error occurred while getting votes: %s" % e)
        raise
    return votes


def get_processed_df(df):
    rate = get_ratings(df)
    votes = get_votes(df)
    new_df = pd.concat([rate, votes], axis=1)
    logging.info("Completed preprocessing")
    return new_df


def preprocess_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    processed_data_path = config["processed_data"]["processed_dataset_csv"]
    df = pd.read_csv(raw_data_path, sep=",")
    logging.info("Starting preprocessing")
    new_df = get_processed_df(df)
    new_df.to_csv(processed_data_path, sep=",", index=False, encoding="utf-8")
    logging.info("Saved preprocessed data!")
    return


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    preprocess_data(config_path=parsed_args.config)
