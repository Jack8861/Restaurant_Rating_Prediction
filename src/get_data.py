import os
import yaml
import pandas as pd
import argparse
import logging


def read_params(config_path):
    """
        reads the params.yaml file
    """
    try:
        with open(config_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
            logging.info("Read config file")
    except OSError as e:
        logging.error("Unable to read config file, Reason: %s" % e)
        raise
    return config


def get_data(config_path):
    """
        gets the data frame
    """
    try:
        config = read_params(config_path)
        data_path = os.path.join("..",config["data_source"]["s3_source"])
        df = pd.read_csv(data_path, sep="|", encoding='utf-8')
        logging.info("Extracted data from csv file")
    except Exception as e:
        logging.error("Could not extract data, Reason: %s" % e)
        raise
    return df


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=os.path.join("..", "params.yaml"))
    parsed_args = args.parse_args()
    data = get_data(config_path=parsed_args.config)
