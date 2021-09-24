from get_data import read_params, get_data
import argparse
import logging
import os

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s', level=logging.INFO, filename=os.path.join('..', 'Training_logs', 'load_data.log'), filemode='w')

def load_and_save(config_path):
    """
        preprocess the column names and put it into raw data path
    """
    try:
        config = read_params(config_path)
        df = get_data(config_path)
        new_cols = [col.replace(" ", "_") for col in df.columns]
        raw_data_path = os.path.join("..", config["load_data"]["raw_dataset_csv"])
        df.to_csv(raw_data_path, sep=",", index=False, header=new_cols)
        logging.info("Cleaned csv file")
    except Exception as e:
        logging.error("Unable to clean data, Reason: %s" % e)
    return


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=os.path.join("..", "params.yaml"))
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)
