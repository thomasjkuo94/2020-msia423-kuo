import os
from config import config
import logging
import argparse

from src.downloads3 import downloads3
from src.clean import clean_data
from src.create_features import create_features

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
    #configurations
    raw_output_filepath = config.AIRBNB_RAW_LOCATION
    clean_output_path = config.CLEAN_OUTPUT_LOCATION
    feature_output_path = config.FEATURE_OUTPUT_LOCATION
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_bucket = config.S3_BUCKET
    s3_path = config.S3_PATH_LOCATION

    parser = argparse.ArgumentParser(description="Download from S3 and clean data, and generate features.")

    #download data from S3
    parser.add_argument('--download', '-d', default=False, action='store_true',
                            help = "If given, download the data from S3 into local")
    #Clean the data after S3 download
    parser.add_argument('--clean', '-c', default=False, action='store_true',
                            help = "If given, clean the data downloaded from S3")
    #Featurize the data
    parser.add_argument('--featurize', '-f', default=False, action='store_true',
                            help = "If given, create features from the clean data")

    args = parser.parse_args()

    if args.download:
        downloads3(access_key, secret_access_key, s3_bucket, s3_path, raw_output_filepath)

    if args.clean:
        try:
            clean_df = clean_data(raw_output_filepath, 
                    config.LISTINGS_DATATYPES, 
                    config.LISTINGS_DROP_COLS,
                    config.VALID_ZIP)
        except Exception:
            logger.error("Something went wrong with clean_data function. Please check raw data and/or configs")
        try:
            clean_df.to_csv(clean_output_path, index=False)
            logger.info("File: {} created -- raw data successfully cleaned".format(clean_output_path))
        except Exception:
            logger.error("Failed to create clean.csv")
            
    if args.featurize:
        try:
            feature_df = create_features(clean_output_path,
                        config.DATA_SCRAPE_DATE,
                        config.HOST_FEATURES,
                        config.PROPERTY_FEATURES,
                        config.BOOKING_FEATURES,
                        config.RESPONSE_VARIABLE)
        except Exception:
            logger.error("Something went wrong with create_features function. Please check cleaned data and/or configs")

        try:
            feature_df.to_csv(feature_output_path, index=False)
            logger.info("File: {} created -- features successfully generated".format(feature_output_path))
        except Exception:
            logger.error("Failed to create feature.csv")
