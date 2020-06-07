import numpy as np
import pandas as pd
import pytest
from src.generate_features import generate_features as gf
from src.generate_features import visible_range as vr
from src.generate_features import visible_norm_range as v_norm
from src.generate_features import log_entropy as log_e
from src.generate_features import entropy_x_contrast as e_x_c
from src.generate_features import ir_range as irr
from src.generate_features import ir_norm_range as ir_norm

def test_visible_range_function_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = vr(input_df)

    true_df = pd.DataFrame([[300],[100]],columns=["visible_range"])

    assert df_test['visible_range'].equals(true_df["visible_range"])

def test_visible_range_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,"400",100,5,5,10,3.5,2,50,40,1],
                        [2,"200",100,11,3,20,4.7,4,300,100,1]], columns=column_names)
    df_test = gf(input_df,column_names,feature_columns)

    assert "visible_range" not in df_test.columns

def test_visible_norm_range_function_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = v_norm(input_df)

    true_df = pd.DataFrame([[100.0],[50.0]],columns=["visible_norm_range"])

    assert df_test['visible_norm_range'].equals(true_df["visible_norm_range"])

def test_visible_norm_range_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([["0",400,100,5,5,10,3.5,2,50,40,1],
                        ["0",200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = gf(input_df,column_names,feature_columns)

    assert "visible_norm_range" not in df_test.columns

def test_log_entropy_function_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = log_e(input_df)

    true_df = pd.DataFrame([[np.log(10)],[np.log(20)]],columns=["log_entropy"])

    assert df_test['log_entropy'].equals(true_df["log_entropy"])

def test_log_entropy_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,"-2",3.5,2,50,40,1],
                        [2,200,100,11,3,"-5",4.7,4,300,100,1]], columns=column_names)

    df_test = gf(input_df,column_names,feature_columns)

    assert "log_entropy" not in df_test.columns

def test_entropy_x_contrast_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = e_x_c(input_df)

    true_df = pd.DataFrame([[5*10],[3*20]],columns=["entropy_x_contrast"])

    assert df_test['entropy_x_contrast'].equals(true_df["entropy_x_contrast"])

def test_entropy_x_contrast_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,None,3.5,2,50,40,1],
                        [2,200,100,11,3,None,4.7,4,300,100,1]], columns=column_names)

    df_test = gf(input_df,column_names,feature_columns)

    assert "entropy_x_contrast" not in df_test.columns

def test_IR_range_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = irr(input_df)

    true_df = pd.DataFrame([[10],[200]],columns=["IR_range"])

    assert df_test['IR_range'].equals(true_df["IR_range"])

def test_IR_range_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,"50",40,1],
                        [2,200,100,11,3,20,4.7,4,"300",100,1]], columns=column_names)

    df_test = gf(input_df,column_names,feature_columns)

    assert "IR_range" not in df_test.columns

def test_IR_norm_range_happy():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,2,50,40,1],
                        [2,200,100,11,3,20,4.7,4,300,100,1]], columns=column_names)

    df_test = ir_norm(input_df)

    true_df = pd.DataFrame([[5.0],[50.0]],columns=["IR_norm_range"])

    assert df_test['IR_norm_range'].equals(true_df["IR_norm_range"])

def test_IR_norm_range_sad():
    column_names = ['visible_mean','visible_max','visible_min','visible_mean_distribution',
      'visible_contrast','visible_entropy','visible_second_angular_momentum','IR_mean',
      'IR_max','IR_min','class']
    feature_columns = ['visible_range','visible_norm_range','log_entropy','entropy_x_contrast',
    'IR_range','IR_norm_range']

    input_df = pd.DataFrame([[3,400,100,5,5,10,3.5,"2",50,40,1],
                        [2,200,100,11,3,20,4.7,"4",300,100,1]], columns=column_names)

    df_test = gf(input_df,column_names,feature_columns)

    assert "IR_norm_range" not in df_test.columns
