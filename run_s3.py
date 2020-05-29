import os
from src.ingestion import fetch_zipfile, gunzip, upload_file_s3
from config import config
import logging

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

if __name__ == '__main__':
    source_file = config.SOURCE_DATA_URL.split("/")[-1]
    output_filepath = config.AIRBNB_RAW_LOCATION
    access_key = os.environ['AWS_ACCESS_KEY_ID']
    secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

    #download gzipped data from InsideAirbnb website
    fetch_zipfile(config.SOURCE_DATA_URL)

    #unzip gzipped file
    gunzip(source_file,output_filepath)

    #upload file to S3
    uploaded = upload_file_s3(output_filepath, config.S3_BUCKET, access_key, secret_access_key, config.S3_PATH_LOCATION)

    if uploaded:
        logger.info("File uploaded to S3 successfully.")
    else:
        print("File upload to S3 was unsuccessful.")
