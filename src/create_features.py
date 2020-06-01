import os
import logging

import numpy as np
import pandas as pd
import datetime
from datetime import date, timedelta

pd.options.mode.chained_assignment = None

#Function to create response variable
def create_response_variable(df):
    """
    A function to create the response variable, a bin of reviews per month
    Input: dataframe
    Output: dataframe with response variable 'reviews_per_month_bin'
    """
    #drop reviews_per_month that are na
    df = df.dropna(subset=["reviews_per_month"])

    #bin 0
    df.loc[:,"reviews_per_month_bin"] = 0
    #bin 1
    df.loc[(df.reviews_per_month > 0) & (df.reviews_per_month <= 0.35), "reviews_per_month_bin"] = 1
    #bin 2
    df.loc[(df.reviews_per_month > 0.35) & (df.reviews_per_month <= 1.1), "reviews_per_month_bin"] = 2
    #bin 3
    df.loc[(df.reviews_per_month > 1.1) & (df.reviews_per_month <= 2.9), "reviews_per_month_bin"] = 3
    #bin 4
    df.loc[(df.reviews_per_month > 2.9), "reviews_per_month_bin"] = 4
    
    return df

#Function create features related to the host
def create_host_features(df, scrape_date):
    '''
    A function to create features related to the airbnb host
    Input: dataframe
    scrape_date: date when data was scraped by inside_airbnb hosts
    Output: dataframe with response variables related to the host
    '''
    #number of years as host
    df.loc[:,"host_since"] = pd.to_datetime(df["host_since"])
    df.loc[:,"years_as_host"] = round((scrape_date - df["host_since"]) / np.timedelta64(1,"Y"), 2)
    
    #convert host response rate to numeric
    df.loc[:,"host_response_rate"] = df["host_response_rate"].str[:-1].astype(float) / 100
    
    #convert host_is_superhost to t = 1, f = 0
    df.loc[df["host_is_superhost"] == "t","host_is_superhost"] = 1
    df.loc[df["host_is_superhost"] == "f","host_is_superhost"] = 0
    
    #convert host_has_profile_pic to t = 1, f = 0
    df.loc[df["host_has_profile_pic"] == "t", "host_has_profile_pic"] = 1
    df.loc[df["host_has_profile_pic"] == "f", "host_has_profile_pic"] = 0
    
    #convert host_identity_verified to t = 1, f = 0
    df.loc[df["host_identity_verified"] == "t", "host_identity_verified"] = 1
    df.loc[df["host_identity_verified"] == "f", "host_identity_verified"] = 0
    
    return df

#Function to create features related to the property
def create_property_features(df):
    '''
    A function to create features related to the airbnb property listing
    Input: dataframe
    Output: dataframe with response variables related to the host
    '''
    #categorize property types
    ppty_categories = {"Apartment","House","Condominium","Guest suite","Boutique hotel","Serviced apartment",
                      "Hotel","Townhouse"}
    df.loc[:,"property_type_cat"] = df["property_type"]
    df.loc[~df["property_type"].isin(ppty_categories),"property_type_cat"] = "Other"
    
    #create bins for accomodates column
    df.loc[:,"accommodates_cat"] = df["accommodates"]
    df.loc[df["accommodates"] <= 2, "accommodates_cat"] = 1
    df.loc[(df["accommodates"] > 2) & (df["accommodates"] <= 4), "accommodates_cat"] = 2
    df.loc[(df["accommodates"] > 4) & (df["accommodates"] <= 6), "accommodates_cat"] = 3
    df.loc[(df["accommodates"] > 6), "accommodates_cat"] = 4
    
    #create bins for the # of bathrooms
    df.loc[:,"bathrooms_cat"] = df["bathrooms"]
    df.loc[(df["bathrooms"] < 2) | (df["bathrooms"].isna()), "bathrooms_cat"] = 1 #if less than 2 or isna
    df.loc[(df["bathrooms"] >= 2) & (df["bathrooms"] < 3), "bathrooms_cat"] = 2
    df.loc[df["bathrooms"] >= 3, "bathrooms_cat"] = 3
    
    #create bins for # of bedrooms
    df.loc[:,"bedrooms_cat"] = df["bedrooms"]
    df.loc[df["bedrooms"].isna(),"bedrooms_cat"] = np.minimum(df["beds"],3) #impute bedrooms based on # of beds
    df.loc[df["bedrooms"] >= 3, "bedrooms_cat"] = 3
    
    #create bins for # of beds--the number of beds is at a minimum, the number of bedrooms
    df.loc[:,"beds_cat"] = df["beds"]
    df.loc[(df["beds"].isna()) | (df["beds"] == 0), "beds_cat"] = np.maximum(df["bedrooms"], 1)
    df.loc[df["beds"] >= 5, "beds_cat"] = 5
    
    #create bins for guests included, those >3 are lumped together
    df.loc[:,"guests_included_cat"] = df["guests_included"]
    df.loc[df["guests_included"] >= 3, "guests_included_cat"] = 3
    
    #turn extra_people into a binary variable. If price >0, then 1
    df.loc[:,"extra_people_cat"] = df["extra_people"]
    df.loc[df["extra_people"] > 0, "extra_people_cat"] = 1
    
    #count the number of amenities, instead of having as text
    df.loc[:,"amenities_count"] = df["amenities"].str[1:-1].str.split(",").str.len()
    
    return df

def create_booking_features(df):
    ''' A function to create features related to booking
    Input: dataframe
    Output: dataframe with response variables related to the booking properties
    '''
    #create bins for minimum nights
    df.loc[:,"minimum_nights_cat"] = df["minimum_nights"]
    df.loc[df["minimum_nights"] <= 7, "minimum_nights_cat"] = 1 #if a week or less, group 1
    df.loc[(df["minimum_nights"] > 7) & (df["minimum_nights"] <= 30), "minimum_nights_cat"] = 2 #if btw. week & month
    df.loc[df["minimum_nights"] > 30, "minimum_nights_cat"] = 3 #greater than a month, 3
    
    #create bins for maximum nights
    df["maximum_nights"] = df["maximum_nights"].astype(int)
    df.loc[:,"maximum_nights_cat"] = df["maximum_nights"]
    df.loc[df["maximum_nights"] <= 30, "maximum_nights_cat"] = 1 #if max is a month or less
    df.loc[(df["maximum_nights"] > 30) & (df["maximum_nights"] <= 365), "maximum_nights_cat"] = 2 #btw. month & year
    df.loc[df["maximum_nights"] > 365, "maximum_nights_cat"] = 3
    
    #change instant_bookable to binary variable, if t=1, f=0
    df.loc[df["instant_bookable"] == "t","instant_bookable"] = 1
    df.loc[df["instant_bookable"] == "f", "instant_bookable"] = 0
    
    #combine super_strict_30, 60, and strict cancellation policies
    df.loc[(df["cancellation_policy"] == "super_strict_30") |
          (df["cancellation_policy"] == "super_strict_60"), "cancellation_policy"] = "strict"
    
    #change require_guest_phone_verification to t=1, f=0
    df.loc[df["require_guest_phone_verification"] == "t", "require_guest_phone_verification"] = 1
    df.loc[df["require_guest_phone_verification"] == "f", "require_guest_phone_verification"] = 0
    
    #change require_guest_profile_picture to t=1, f=0
    df.loc[df["require_guest_profile_picture"] == "t", "require_guest_profile_picture"] = 1
    df.loc[df["require_guest_profile_picture"] == "f", "require_guest_profile_picture"] = 0
    
    return df

def clean_data_types(df):
    """Clean up datatypes of final dataset
    input: dataframe
    output: final dataframe with clean types
    """
    df["host_is_superhost"] = df["host_is_superhost"].astype(int)
    df["host_has_profile_pic"] = df["host_has_profile_pic"].astype(int)
    df["host_identity_verified"] = df["host_identity_verified"].astype(int)
    df["host_listings_count"] = df["host_listings_count"].astype(int)
    df["room_type"] = df["room_type"].astype(str)
    df["property_type_cat"] = df["property_type_cat"].astype(str)
    df["bathrooms_cat"] = df["bathrooms_cat"].astype(int)
    df["bedrooms_cat"] = df["bedrooms_cat"].astype(int)
    df["beds_cat"] = df["beds_cat"].astype(int)
    df["extra_people_cat"] = df["extra_people_cat"].astype(int)
    df["instant_bookable"] = df["instant_bookable"].astype(int)
    df["cancellation_policy"] = df["cancellation_policy"].astype(str)
    df["require_guest_phone_verification"] = df["require_guest_phone_verification"].astype(int)
    df["require_guest_profile_picture"] = df["require_guest_profile_picture"].astype(int)
    
    return df

def create_features(clean_datapath, scrape_date, host_features,
					property_features, booking_features, response_variable):
    '''Create features related to host, property, booking, and response
    
    Args:
        clean_datapath (str): file path for cleaned data
        scrape_date (datetime): the date when inside_airbnb scraped data
    	host_features (list): a list of the columns to keep for host features
    	property_features (list): a list of of the columns to keep for property features
    	booking_features (list): a list of of the columns to keep for booking features
    	response_variable (list): a list of length 1 of the response variable

    Returns:
        df (dataframe object): cleaned dataframe
    '''

    df = pd.read_csv(clean_datapath)
    df = create_response_variable(df)
    df = create_host_features(df, scrape_date)
    df = create_property_features(df)
    df = create_booking_features(df)
    
    #select final variables
    df = df[host_features+
            property_features+
            booking_features+
            response_variable]

    df = clean_data_types(df)
    
    return df
