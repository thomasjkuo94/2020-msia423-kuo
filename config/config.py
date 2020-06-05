from os import path
import datetime
from scipy import stats
import numpy as np

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
#CREATE_RDS = False

# cleaning script configurations
CLEAN_OUTPUT_LOCATION = path.join(PROJECT_HOME,'data/clean.csv')
LISTINGS_DATATYPES = {
    "zipcode": "str",
    "price": "str",
    "weekly_price": "str",
    "monthly_price": "str",
    "security_deposit": "str",
    "cleaning_fee": "str"
}
LISTINGS_DROP_COLS = {
    "scrape_id",
    "last_scraped",
    "listing_url",
    "experiences_offered",
    "thumbnail_url",
    "medium_url",
    "picture_url",
    "xl_picture_url",
    "host_url",
    "host_thumbnail_url",
    "host_picture_url",
    "latitude",
    "longitude",
    "is_location_exact",
    "calendar_last_scraped",
    "license",
    "jurisdiction_names",
    "host_acceptance_rate",
    "neighbourhood_group_cleansed",
    "neighbourhood",
    "market",
}
VALID_ZIP = {
    "94101",
    "94102",
    "94103",
    "94104",
    "94105",
    "94107",
    "94108",
    "94109",
    "94110",
    "94111",
    "94112",
    "94114",
    "94115",
    "94116",
    "94117",
    "94118",
    "94119",
    "94120",
    "94121",
    "94122",
    "94123",
    "94124",
    "94125",
    "94126",
    "94127",
    "94129",
    "94130",
    "94131",
    "94132",
    "94133",
    "94134",
    "94137",
    "94139",
    "94140",
    "94141",
    "94142",
    "94143",
    "94144",
    "94145",
    "94146",
    "94147",
    "94151",
    "94153",
    "94154",
    "94156",
    "94158",
    "94159",
    "94160",
    "94161",
    "94162",
    "94163",
    "94164",
    "94171",
    "94172",
    "94177",
    "94188"
}

#featurize configurations
DATA_SCRAPE_DATE = datetime.datetime(2020, 1, 4)
FEATURE_OUTPUT_LOCATION = path.join(PROJECT_HOME,'data/features.csv')
RESPONSE_VARIABLE = ["reviews_per_month_bin"]
HOST_FEATURES = [
    "years_as_host",
    "host_response_time",
    "host_response_rate",
    "host_is_superhost",
    "host_has_profile_pic",
    "host_identity_verified",
    "host_listings_count"
]
PROPERTY_FEATURES = [
    "room_type",
    "property_type_cat",
    "accommodates_cat",
    "bathrooms_cat",
    "bedrooms_cat",
    "beds_cat",
    "guests_included_cat",
    "extra_people_cat",
    "price",
    "security_deposit",
    "cleaning_fee",
    "amenities_count",
    "neighbourhood_cleansed"
]
BOOKING_FEATURES = [
    "minimum_nights_cat",
    "maximum_nights_cat",
    "instant_bookable",
    "cancellation_policy",
    "require_guest_phone_verification",
    "require_guest_profile_picture"
]

#Training Full Model
IMPUTED_OUTPUT_LOCATION = path.join(PROJECT_HOME,'data/imputed.csv')
SCORES_OUTPUT_LOCATION = path.join(PROJECT_HOME,'data/params_and_scores.txt')
SAVED_MODEL_LOCATION = path.join(PROJECT_HOME,'data/trained_model.sav')
SAVED_ENCODER_LOCATION = path.join(PROJECT_HOME,'data/encoder.sav')
RANDOM_STATE = 1414
BEST_LR = 0.06144119459702984
BEST_NUM_EST = 525
BEST_MAX_DEPTH = 5
BEST_SUBSAMPLE = 0.5

#Tuning Hyperparameters
TUNING_GRID = {
    "learning_rate": stats.uniform(loc=0, scale=0.2),
    "n_estimators": np.arange(25, 750, 25),
    "max_depth": [3, 5, 8, 10, 15, 20],
    "subsample": [0.2, 0.3, 0.5, 0.7, 0.9]
}
TEST_SIZE = 0.1
NUM_ITERS = 25 
N_JOBS = -2
PARAM_SCORING = ["roc_auc_ovo","accuracy"]
GRID_REFIT = "roc_auc_ovo"
