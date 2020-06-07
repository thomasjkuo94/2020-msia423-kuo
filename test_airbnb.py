import numpy as np
import pandas as pd
import pytest
import datetime
from datetime import date, timedelta

from src.clean import clean_zips
from src.create_features import create_response_variable
from src.create_features import bool_to_int
from src.create_features import percent_to_dec
from src.create_features import years_since
from src.create_features import extract_str_count


def test_clean_zips_happy():
    column_names = ['zipcode']
    zips = ["91889"]

    input_df = pd.DataFrame([["CA 91889"],
                        ["91888"]], columns=column_names)

    df_test = clean_zips(input_df,zips)

    true_df = pd.DataFrame([["91889"],[np.nan]],columns=column_names)

    assert df_test["zipcode"].equals(true_df["zipcode"])

def test_clean_zips_sad():
    column_names = ['zipcode']
    zips = ["91889"]

    input_df = pd.DataFrame([["CAC 91889"],
                        ["91888"]], columns=column_names)

    df_test = clean_zips(input_df,zips)

    true_df = pd.DataFrame([["91889"],[np.nan]],columns=column_names)

    assert ~(df_test["zipcode"].equals(true_df["zipcode"]))

def test_create_response_happy():
    column_names = ['reviews_per_month']

    input_df = pd.DataFrame([[1.7],
                        [0.3]], columns=column_names)

    df_test = create_response_variable(input_df)

    true_df = pd.DataFrame([[3],[1]],columns=["reviews_per_month_bin"])

    assert df_test["reviews_per_month_bin"].equals(true_df["reviews_per_month_bin"])

def test_bool_to_int_happy():
    column_names = ['truefalse']

    input_df = pd.DataFrame([["t"]], columns=column_names)

    df_test = bool_to_int(input_df,"truefalse")

    true_df = pd.DataFrame([[1]],columns=column_names)

    assert df_test["truefalse"][0] == (true_df["truefalse"][0])

def test_percent_to_dec_happy():
    column_names = ['percdec']

    input_df = pd.DataFrame([["85%"],
                              ["100%"]], columns=column_names)

    df_test = percent_to_dec(input_df,"percdec")

    true_df = pd.DataFrame([[0.85],
                            [1.00]],columns=column_names)

    assert df_test["percdec"].equals(true_df["percdec"])

def test_years_since_happy():
    column_names = ['years_since']
    scrape = datetime.datetime(2020, 1, 4)

    input_df = pd.DataFrame([["7/31/2008"]], columns=column_names)

    df_test = years_since(input_df,"years_since",scrape)

    true_df = pd.DataFrame([[11.43]],columns=["years_as_host"])

    assert df_test["years_as_host"].equals(true_df["years_as_host"])

def test_extract_str_count_happy():
    column_names = ['amenities_list']

    input_df = pd.DataFrame([["{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}"]], columns=column_names)

    df_test = extract_str_count(input_df,"amenities_list")

    true_df = pd.DataFrame([[26]],columns=["amenities_count"])

    assert df_test["amenities_count"].equals(true_df["amenities_count"])
