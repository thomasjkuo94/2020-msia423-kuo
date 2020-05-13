from os import path

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "airbnb_db"
DEBUG = True

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Local Database connection config
DATABASE_PATH = path.join(PROJECT_HOME, 'data/airbnb_db.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# API configs - TODO FOR FLASK
HOST = "host.docker.internal"
PORT = 5000
API_SENTIMENT_PATH = 'sentiment'
API_ENDPOINT = "http://{}:{}/{}".format(HOST, PORT, API_SENTIMENT_PATH)

# s3 configurations for ingestion and pushing to bucket
SOURCE_DATA_URL = "http://data.insideairbnb.com/united-states/ca/san-francisco/2020-01-04/data/listings.csv.gz"
AIRBNB_RAW_LOCATION = path.join(PROJECT_HOME,'data/listings.csv')
S3_BUCKET = "nw-tkj775-s3"
S3_PATH_LOCATION = "data/listings.csv"