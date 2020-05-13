import os
import sys
from config import config
import logging

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData, Float, Text

import argparse
from src.helpers import create_connection, get_session


#environment variables
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")
engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)


# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

#argparse
parser = argparse.ArgumentParser(description="Create defined tables in database, and select local or AWS database push")
parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from abb_feat_and_resp table before create_all "
                            "so that table can be recreated without unique id issues ")
parser.add_argument("--local", "-l", default=False, action="store_true",
                        help="If given, push data to local sql database")
parser.add_argument("--rds", "-r", default=False, action="store_true",
                        help="If given, push data to AWS RDS database")
args = parser.parse_args()

Base = declarative_base()  

class Airbnb(Base):
    """Create a data model for the database to be set up for capturing songs """
    __tablename__ = 'abb_feat_and_resp'
    id = Column(Integer, primary_key=True)
    years_as_host = Column(Float, unique=False, nullable=True)
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
    minimum_nights_cat = Column(Integer, unique=False, nullable=True)
    maximum_nights_cat = Column(Integer, unique=False, nullable=True)
    instant_bookable = Column(Integer, unique=False, nullable=True)
    cancellation_policy = Column(String(100), unique=False, nullable=True)
    require_guest_phone_verification = Column(String(100), unique=False, nullable=True)
    require_guest_profile_picture = Column(String(100), unique=False, nullable=True)
    review_per_month_bin = Column(Integer, unique=False, nullable=True)
      
    def __repr__(self):
        return '<Airbnb %r>' % self.id

def _truncate_abb(session):
    """Deletes tweet scores table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM abb_feat_and_resp''')


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base` (Airbnb).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Base.metadata.create_all(engine)

if __name__ == '__main__':
    #if user chooses rds as argument
    if args.rds:
        logger.info("Airbnb Database location: AWS RDS")
        # set up mysql connection
        engine = sql.create_engine(engine_string)

        # create the tracks table
        Base.metadata.create_all(engine)

        # create a db session
        Session = sessionmaker(bind=engine)  
        session = Session()
        logger.info("Airbnb Database created in AWS RDS")

        """ TODO: Once data is finalized and ready to be pushed, modify this appropriately.
        # add a record/track
        track1 = Airbnb(artist="Britney Spears", album="Circus", title="Radar")  
        session.add(track1)
        session.commit()

        logger.info("Database created with song added: Radar by Britney spears from the album, Circus")  
        track2 = Airbnb(artist="Tayler Swift", album="Red", title="Red")  
        session.add(track2)

        # To add multiple rows
        # session.add_all([track1, track2])


        session.commit()   
        logger.info("Database created with song added: Red by Tayler Swift from the album, Red")

        # query records
        track_record = session.query(Airbnb.title, Airbnb.album).filter_by(artist="Britney Spears").first() 
        print(track_record)

        query = "SELECT * FROM tracks WHERE artist LIKE '%%Britney%%'"
        result = session.execute(query)
        print(result.first().items())
        """

        session.close()

    #if user chooses local as argument
    elif args.local:
        logger.info("Airbnb Database location: local database")

        # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the abb_feat_and_resp table)
        if args.truncate:
            session = get_session(engine_string=config.SQLALCHEMY_DATABASE_URI)
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

        create_db(engine_string=config.SQLALCHEMY_DATABASE_URI)

    else:
        logger.info("Please pass a valid argument: --local, --l for local & --rds, -r for rds")
