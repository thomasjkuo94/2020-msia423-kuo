import os
import logging

import numpy as np
import pandas as pd

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
    
    #drop unused columns
    df = df.drop(columns=dropped_cols, axis=1)
    
    #drop observations that have no relevant host info
    df = df.dropna(subset=["host_since",
                          "host_response_rate",
                          "host_is_superhost",
                          "host_listings_count"],
                    how="all")
    
    #extract zipcode and set invalid zipcodes as NaN
    df.zipcode = df.zipcode.str.replace("CA ","")
    df.zipcode = df.zipcode.replace("CA", np.nan)
    df.loc[~df.zipcode.isin(zipcodes), "zipcode"] = np.nan
    
    #change price to a float
    df.price = df.price.str.replace(",","").str[1:].astype(float)
    
    #change weekly_price to a float
    df.weekly_price = df.weekly_price.str.replace(",","").str[1:].astype(float)
    
    #change monthly_price to a float
    df.monthly_price = df.monthly_price.str.replace(",","").str[1:].astype(float)
    
    #change security_deposit to a float
    df.security_deposit = df.security_deposit.str.replace(",","").str[1:].astype(float)
    
    #change cleaning_fee to a float
    df.cleaning_fee = df.cleaning_fee.str.replace(",","").str[1:].astype(float)
    
    #change extra_people to a float
    df.extra_people = df.extra_people.str.replace(",","").str[1:].astype(float)

    #drop reviews_per_month that are na
    df = df.dropna(subset=["reviews_per_month"])
    
    return df
