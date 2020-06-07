import os
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def clean_data(raw_input_path, listing_types, dropped_cols, zipcodes):
    '''Clean raw data and return a dataframe of cleaned data
    
    Args:
        raw_input_path (str): file path for raw input data downloaded from S3
        listing_types (dict): a dictionary of listing types that need to be cast
    	dropped_cols (dict): a list of the columns that aren't needed
    	zipcodes (dict): a list of valid San Francisco zipcodes

    Returns:
        df (dataframe object): cleaned dataframe
    '''

    df = pd.read_csv(raw_input_path, dtype=listing_types)

    price_columns = ["price","weekly_price","monthly_price","security_deposit",
                    "cleaning_fee","extra_people"]
    
    #drop unused columns
    df = df.drop(columns=dropped_cols, axis=1)
    
    #drop observations that have no relevant host info
    df = df.dropna(subset=["host_since",
                          "host_response_rate",
                          "host_is_superhost",
                          "host_listings_count"],
                    how="all")
    
    #extract zipcode and set invalid zipcodes as NaN
    try:
        df = clean_zips(df, zipcodes)
    except Exception as e:
        logger.error(e)

    #clean columns related to pricing metrics
    for col in price_columns:
        try:
            df = clean_pricing(df, col)
        except Exception as e:
            logger.error(e)

    #drop reviews_per_month that are na
    df = df.dropna(subset=["reviews_per_month"])
    
    return df

def clean_zips(df, zipcodes):
    '''Clean zipcodes in rawdata
    
    Args:
        df (dataframe object)): dataframe to be cleaned
        zipcodes (dict): a list of valid San Francisco zipcodes

    Returns:
        df (dataframe object): cleaned dataframe
    '''
    df.zipcode = df.zipcode.str.replace("CA ","")
    df.zipcode = df.zipcode.replace("CA", np.nan)
    df.loc[~df.zipcode.isin(zipcodes), "zipcode"] = np.nan

    return df

def clean_pricing(df,col_name):
    '''Clean pricing variables in rawdata by removing $ and commas
    
    Args:
        df (dataframe object)): dataframe to be cleaned
        col_name (string): column name of column to be cleaned

    Returns:
        df (dataframe object): cleaned dataframe
    '''
    df[col_name] = df[col_name].str.replace(",","").str[1:].astype(float)

    return df
