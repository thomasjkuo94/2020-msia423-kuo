import traceback
from flask import render_template, request, redirect, url_for
from config import config
import pandas as pd
import numpy as np
import logging.config
import pickle
from flask import Flask
from run_database import Airbnb
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        listings = db.session.query(Airbnb).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', abb_feat_and_resp=listings)
    except:
        traceback.print_exc()
        logger.warning("Not able to display listings, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try: 
        categorical_columns = ["host_response_time",
                            "room_type",
                            "property_type_cat",
                          "neighbourhood_cleansed",
                          "cancellation_policy"]

        #save input
        years_as_host = float(request.form['years_as_host'])
        host_response_time = request.form['host_response_time']
        host_response_rate = float(request.form['host_response_rate'])
        host_is_superhost = int(request.form['host_is_superhost'])
        host_has_profile_pic = int(request.form['host_has_profile_pic'])
        host_identity_verified = int(request.form['host_identity_verified'])
        host_listings_count = int(request.form['host_listings_count'])
        room_type = request.form['room_type']
        property_type_cat = request.form['property_type_cat']
        accommodates_cat = int(request.form['accommodates_cat'])
        bathrooms_cat = int(request.form['bathrooms_cat'])
        bedrooms_cat = int(request.form['bedrooms_cat'])
        beds_cat = int(request.form['beds_cat'])
        guests_included_cat = int(request.form['guests_included_cat'])
        extra_people_cat = int(request.form['extra_people_cat'])
        price = float(request.form['price'])
        security_deposit = float(request.form['security_deposit'])
        cleaning_fee = float(request.form['cleaning_fee'])
        amenities_count = int(request.form['amenities_count'])
        neighbourhood_cleansed = request.form['neighbourhood_cleansed']
        minimum_nights_cat = int(request.form['minimum_nights_cat'])
        maximum_nights_cat = int(request.form['maximum_nights_cat'])
        instant_bookable = int(request.form['instant_bookable'])
        cancellation_policy = request.form['cancellation_policy']
        require_guest_phone_verification = int(request.form['require_guest_phone_verification'])
        require_guest_profile_picture = int(request.form['require_guest_profile_picture'])

        #dataframe
        df_entry = pd.DataFrame(
            {
               "years_as_host": years_as_host,
                "host_response_time": host_response_time,
                "host_response_rate": host_response_rate,
                "host_is_superhost": host_is_superhost,
                "host_has_profile_pic": host_has_profile_pic,
                "host_identity_verified": host_identity_verified,
                "host_listings_count": host_listings_count,
                "room_type": room_type,
                "property_type_cat": property_type_cat,
                "accommodates_cat": accommodates_cat,
                "bathrooms_cat": bathrooms_cat,
                "bedrooms_cat": bedrooms_cat,
                "beds_cat": beds_cat,
                "guests_included_cat": guests_included_cat,
                "extra_people_cat": extra_people_cat,
                "price": price,
                "security_deposit": security_deposit,
                "cleaning_fee": cleaning_fee,
                "amenities_count": amenities_count,
                "neighbourhood_cleansed": neighbourhood_cleansed,
                "minimum_nights_cat": minimum_nights_cat,
                "maximum_nights_cat": maximum_nights_cat,
                "instant_bookable": instant_bookable,
                "cancellation_policy": cancellation_policy,
                "require_guest_phone_verification": require_guest_phone_verification,
                "require_guest_profile_picture": require_guest_profile_picture,
                "reviews_per_month_bin": "very popular"
            },
            index=np.arange(0,1)
        )

        #load trained model & encoder
        trained_model = pickle.load(open(config.SAVED_MODEL_LOCATION, 'rb'))
        encoder = pickle.load(open(config.SAVED_ENCODER_LOCATION, 'rb'))

        #predict on df_entry
        df_predict = df_entry.loc[:, df_entry.columns != "reviews_per_month_bin"]
        df_onehot_predict = pd.DataFrame(
            encoder.transform(df_entry[categorical_columns]).toarray(),
            columns = encoder.get_feature_names(categorical_columns)
        )
        df_predict = df_predict.join(df_onehot_predict).drop(columns=categorical_columns)

        entry_prediction = trained_model.predict(df_predict)

        reviews_per_month_bin = map_bin(int(entry_prediction[0]))
        logger.info("Prediction successful!")

        listings1 = Airbnb(years_as_host = years_as_host, host_response_time = host_response_time,
                            host_response_rate = host_response_rate, host_is_superhost = host_is_superhost,
                            host_has_profile_pic = host_has_profile_pic, host_identity_verified = host_identity_verified,
                            host_listings_count = host_listings_count, room_type = room_type, property_type_cat = property_type_cat,
                            accommodates_cat = accommodates_cat, bathrooms_cat = bathrooms_cat, bedrooms_cat = bedrooms_cat,
                            beds_cat = beds_cat, guests_included_cat = guests_included_cat, extra_people_cat = extra_people_cat,
                            price = price, security_deposit = security_deposit, cleaning_fee = cleaning_fee,
                            amenities_count = amenities_count, neighbourhood_cleansed = neighbourhood_cleansed,
                            minimum_nights_cat = minimum_nights_cat, maximum_nights_cat = maximum_nights_cat,
                            instant_bookable = instant_bookable, cancellation_policy = cancellation_policy,
                            require_guest_phone_verification = require_guest_phone_verification,
                            require_guest_profile_picture = require_guest_profile_picture, reviews_per_month_bin = reviews_per_month_bin
                            )
        db.session.add(listings1)
        db.session.commit()
        logger.info("New listing successfully added!")

        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display listings, error page returned")
        return render_template('error.html')

def map_bin(x):
    if x == 1:
        return "very unpopular"
    elif x == 2:
        return "unpopular"
    elif x == 3:
        return "popular"
    elif x == 4:
        return "very popular"
    else:
        return "somethings wrong"

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])