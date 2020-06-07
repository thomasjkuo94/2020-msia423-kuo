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
        downloads3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
                                     config.S3_BUCKET, config.S3_PATH_LOCATION, config.AIRBNB_RAW_LOCATION)

    if args.clean:
        try:
            clean_df = clean_data(config.AIRBNB_RAW_LOCATION, 
                    config.LISTINGS_DATATYPES, 
                    config.LISTINGS_DROP_COLS,
                    config.VALID_ZIP)
        except Exception:
            logger.error("Something went wrong with clean_data function. Please check raw data and/or configs")
        try:
            clean_df.to_csv(config.CLEAN_OUTPUT_LOCATION, index=False)
            logger.info("File: {} created -- raw data successfully cleaned".format(config.CLEAN_OUTPUT_LOCATION))
        except Exception:
            logger.error("Failed to create clean.csv")
            
    if args.featurize:
        try:
            feature_df = create_features(config.CLEAN_OUTPUT_LOCATION,
                        config.DATA_SCRAPE_DATE,
                        config.HOST_FEATURES,
                        config.PROPERTY_FEATURES,
                        config.BOOKING_FEATURES,
                        config.RESPONSE_VARIABLE)
        except Exception:
            logger.error("Something went wrong with create_features function. Please check cleaned data and/or configs")

        try:
            feature_df.to_csv(config.FEATURE_OUTPUT_LOCATION, index=False)
            logger.info("File: {} created -- features successfully generated".format(config.FEATURE_OUTPUT_LOCATION))
        except Exception:
            logger.error("Failed to create feature.csv")
