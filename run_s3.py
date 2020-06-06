import os
from src.ingestion import fetch_zipfile, gunzip, upload_file_s3
from config import config
import logging

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

if __name__ == '__main__':
    #download gzipped data from InsideAirbnb website
    fetch_zipfile(config.SOURCE_DATA_URL)

    #unzip gzipped file
    gunzip(config.SOURCE_DATA_URL.split("/")[-1],config.AIRBNB_RAW_LOCATION)

    #upload file to S3
    uploaded = upload_file_s3(config.AIRBNB_RAW_LOCATION, config.S3_BUCKET, os.environ.get('AWS_ACCESS_KEY_ID'),
                                 os.environ.get('AWS_SECRET_ACCESS_KEY'), config.S3_PATH_LOCATION)

    if uploaded:
        logger.info("File uploaded to S3 successfully.")
    else:
        logger.error("File upload to S3 was unsuccessful.")
