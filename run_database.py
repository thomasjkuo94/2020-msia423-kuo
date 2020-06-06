import os
import sys
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
import logging

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData, Float, Text

import argparse

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

#argparse
parser = argparse.ArgumentParser(description="Create defined tables in database, and select local or AWS database push")
parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from abb_feat_and_resp table before create_all "
                            "so that table can be recreated without unique id issues ")

args = parser.parse_args()

Base = declarative_base()  

class Airbnb(Base):
    """Create a data model for the database to be set up for capturing features related to Airbnb listings in San Francisco """
    __tablename__ = 'abb_feat_and_resp'
    id = Column(Integer, primary_key=True)
    years_as_host = Column(Float, unique=False, nullable=True)
    host_response_time = Column(String(100), unique=False, nullable=True)
    host_response_rate = Column(Float, unique=False, nullable=True)
    host_is_superhost = Column(Integer, unique=False, nullable=True)
    host_has_profile_pic = Column(Integer, unique=False, nullable=True)
    host_identity_verified = Column(Integer, unique=False, nullable=True)
    host_listings_count = Column(Integer, unique=False, nullable=True)
    room_type = Column(String(100), unique=False, nullable=True)
    property_type_cat = Column(String(100), unique=False, nullable=True)
    accommodates_cat = Column(Integer, unique=False, nullable=True)
    bathrooms_cat = Column(Integer, unique=False, nullable=True)
    bedrooms_cat = Column(Integer, unique=False, nullable=True)
    beds_cat = Column(Integer, unique=False, nullable=True)
    guests_included_cat = Column(Integer, unique=False, nullable=True)
    extra_people_cat = Column(Integer, unique=False, nullable=True)
    price = Column(Float, unique=False, nullable=True)
    security_deposit = Column(Float, unique=False, nullable=True)
    cleaning_fee = Column(Float, unique=False, nullable=True)
    amenities_count = Column(Integer, unique=False, nullable=True)
    neighbourhood_cleansed = Column(String(100), unique=False, nullable=True)
    minimum_nights_cat = Column(Integer, unique=False, nullable=True)
    maximum_nights_cat = Column(Integer, unique=False, nullable=True)
    instant_bookable = Column(Integer, unique=False, nullable=True)
    cancellation_policy = Column(String(100), unique=False, nullable=True)
    require_guest_phone_verification = Column(Integer, unique=False, nullable=True)
    require_guest_profile_picture = Column(Integer, unique=False, nullable=True)
    reviews_per_month_bin = Column(String(100), unique=False, nullable=True)
      
    def __repr__(self):
        return '<Airbnb %r>' % self.id

def _truncate_abb(session):
    """Deletes abb_feat_and_resp table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM abb_feat_and_resp''')

if __name__ == '__main__':
    if os.environ.get('MYSQL_HOST') is None:
        logger.info("Airbnb Database location: Local")
    else:
        logger.info("Airbnb Database location: AWS RDS")
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    if args.truncate:
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            logger.info("Attempting to truncate abb_feat_and_resp table.")
            _truncate_abb(session)
            session.commit()
            logger.info("abb_feat_and_resp truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate abb_feat_and_resp table.")
            logger.error(e)
        finally:
            session.close()

    # create the airbnb table
    Base.metadata.create_all(engine)

    logger.info("Airbnb Database created successfully!")

