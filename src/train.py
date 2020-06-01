import os
import logging

import pandas as pd
import numpy as np
import math
from scipy import stats

#Imputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

#Model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import OneHotEncoder

def get_model_data(features_path, seed):
    '''Impute missing feature input: security_deposit, cleaning_fee, host_response_time, and host_response_rate
    
    Args:
        features_path (str): a string pointing to features.csv
        seed (int): a seed to set for random_state to preserve reproducibility

    Returns:
        df (dataframe object): dataframe with features imputed and ready for model
    '''
    df = pd.read_csv(features_path)

    #impute values for security_deposit and cleaning_fee using median
    df["security_deposit"] = df["security_deposit"].fillna(value = df["security_deposit"].median())
    df["cleaning_fee"] = df["cleaning_fee"].fillna(value = df["cleaning_fee"].median())
    df = df.reset_index(drop=True)

    #map host_response_time to numerical values and drop text
    host_resp_map = {
        "within an hour": 0,
        "within a few hours": 1,
        "within a day": 2,
        "a few days or more": 3,
    }
    inv_host_resp_map = dict([[v,k] for k,v in host_resp_map.items()])

    #impute df to copy values over to original df
    imputed_df = impute_missing(df, seed, host_resp_map)

    df = df[[c for c in df if c not in ["reviews_per_month_bin"]] 
           + ["reviews_per_month_bin"]]

    df.loc[:,"host_response_rate"] = imputed_df.loc[:,"host_response_rate"]
    df.loc[:,"host_response_time"] = imputed_df.loc[:,"host_response_time_mapping"].map(inv_host_resp_map)

    model_df = df

    return model_df

def impute_missing(final_df, seed, host_resp_map):
    '''Helper function to preserve features dataframe while imputing values
    
    Args:
        final_df (dataframe): a dataframe with features that still need imouting
        seed (int): a seed to set for random_state to preserve reproducibility
        host_resp_map (dict): a dictionary of values to map host_response_time to numerical

    Returns:
        df (dataframe object): dataframe with features imputed to be transfered to features df
    '''
    #one-hot encode categorical variables before imputing
    final_df = pd.get_dummies(
        final_df,
        columns=[
            "room_type",
            "property_type_cat",
            "neighbourhood_cleansed",
            "cancellation_policy",
        ],
        prefix=[
            "room_type",
            "property_type",
            "neighbourhood",
            "cancellation_policy",
        ],
        drop_first=True,
    )

    final_df.loc[:, "host_response_time_mapping"] = final_df["host_response_time"].map(host_resp_map)
    final_df = final_df.drop("host_response_time",axis=1)
    

    #IterativeImputer parameters
    imputer = IterativeImputer(max_iter = 12,
                               random_state=seed,
                               verbose=0,
                               initial_strategy="most_frequent")

    #Impute columns that aren't response
    imputation_df = final_df.drop("reviews_per_month_bin",axis=1)

    #Imputation columns
    imp_columns = imputation_df.columns.tolist()

    imputed = pd.DataFrame(imputer.fit_transform(imputation_df), columns=imp_columns)
    
    #round imputed host_response_time_mapping(categorical):
    #if greater than 3, round to 3, if less than 0 round to 0
    imputed.loc[:,"host_response_time_mapping"] = imputed["host_response_time_mapping"].round(decimals=0)
    imputed.loc[imputed["host_response_time_mapping"] < 0,"host_response_time_mapping"] = 0
    imputed.loc[imputed["host_response_time_mapping"] > 3,"host_response_time_mapping"] = 3

    #round imputed host_response_rate:
    #if greater than 1, round to 1, else round to 2 decimal places
    #if less than 0, round to 0
    imputed.loc[:,"host_response_rate"] = imputed["host_response_rate"].round(decimals = 2)
    imputed.loc[imputed["host_response_rate"] > 1,"host_response_rate"] = 1.00
    imputed.loc[imputed["host_response_rate"] < 0,"host_response_rate"] = 0
    
    model_df = pd.merge(imputed, final_df[["reviews_per_month_bin"]].reset_index(drop=True),
                   left_index=True, right_index=True)
    
    return model_df

def tune_and_score(imputed_filepath, seed, tuning_grid, 
                    num_iters, n_jobs, param_scoring, grid_refit, test_size):
    '''Train hyperparams on final imputed model data
    
    Args:
        imputed_filepath (str): file path to final imputed model data
        seed (int): a seed to set for random_state to preserve reproducibility
        tuning_grid(dict): a dictionary for chosen hyperparams
        num_iters (int): number of iterations to run gridsearch
        n_jobs (int): number of CPUs to use
        param_scoring (str or list): type of scoring methodology
        grid_refit(str): what to refit best parameters on
        test_size(float): between 0 & 1, percentage of obs in test set


    Returns:
        search_gbt (classifier): to extract best hyperparameters
        cv_auc (float): cross-validation AUC
        cv_accu (float): cross-validation accuracy
        test_auc (float): test AUC
        test_accu (float): test accuracy
    '''
    df = pd.read_csv(imputed_filepath)

    df = one_hot_encode(df)

    #get predictors and response of the dataset
    predictors = df.loc[:, df.columns != "reviews_per_month_bin"]
    response = df.loc[:, "reviews_per_month_bin"]

    X_train, X_test, y_train, y_test = train_test_split(predictors, response, test_size=test_size, random_state=seed)

    # Model
    estimator_gbt = GradientBoostingClassifier(n_iter_no_change=3, random_state=seed)

    # RandomizedSearch with 5-fold (default)
    clf_gbt = RandomizedSearchCV(estimator_gbt, tuning_grid, n_iter=num_iters, random_state=seed, n_jobs=n_jobs,
                                 scoring=param_scoring, refit=grid_refit)
    # Randomized Search on Predictors & Response
    search_gbt = clf_gbt.fit(X_train, y_train)
    print("Best Hyperparameters:", search_gbt.best_params_)
    cv_auc = search_gbt.best_score_
    cv_accu = max(search_gbt.cv_results_['mean_test_accuracy'])
    print("CV AUC:", cv_auc)
    print("CV Accuracy:", cv_accu)

    test_auc, test_accu = test_metrics(search_gbt, X_test, y_test, seed)
    return search_gbt, cv_auc, cv_accu, test_auc, test_accu

def one_hot_encode(df):
    '''A function to one-hot encode certain categorical variables
    
    Args:
        df(dataframe): dataframe of imputed data

    Returns:
        encoded_df (dataframe): one-hot encoded dataframe
    '''
    categorical_columns = ["host_response_time",
                            "room_type",
                            "property_type_cat",
                          "neighbourhood_cleansed",
                          "cancellation_policy"]
    #define encoder
    encoder = OneHotEncoder(drop="first")
    #fit to categorical columns
    encoder.fit(df[categorical_columns])

    encoded_df = df
    df_onehot = pd.DataFrame(
        encoder.transform(df[categorical_columns]).toarray(),
        columns = encoder.get_feature_names(categorical_columns)
    )
    encoded_df = encoded_df.join(df_onehot).drop(columns=categorical_columns)

    encoded_df = encoded_df[[c for c in encoded_df if c not in ["reviews_per_month_bin"]] 
           + ["reviews_per_month_bin"]]
    
    return encoded_df

def test_metrics(classifier, predictors, response, seed):
    '''Score classifier on test set
    
    Args:
        classifier (classifier object): classifier to extract best hyperparams
        predictors (dataframe): a dataframe of predictors representing test set
        response (dataframe): a dataframe of responses representing test set
        seed (int): a seed to maintain reproducibility

    Returns:
        test_auc (float): test AUC
        test_accu (float): test accuracy
    '''
    learning_gbt = classifier.best_params_["learning_rate"]
    n_estimators_gbt = classifier.best_params_["n_estimators"]
    max_depth_gbt = classifier.best_params_["max_depth"]
    subsample_gbt = classifier.best_params_["subsample"]

    final_gbt = GradientBoostingClassifier(
        learning_rate=learning_gbt,
        n_estimators=n_estimators_gbt,
        max_depth=max_depth_gbt,
        subsample=subsample_gbt,
        n_iter_no_change=3,
        random_state = seed
    )

    results = final_gbt.fit(predictors,response)
    #Test Metrics
    resp_prob = results.predict_proba(predictors)
    test_auc = roc_auc_score(response, resp_prob, multi_class="ovo", average="macro")
    test_accu = results.score(predictors,response)
    print("Test AUC: ", test_auc)
    print("Test Accuracy: ", test_accu)
    return test_auc, test_accu

def train_model(imputed_filepath, seed, best_lr, best_numest, best_maxd, best_subsamp):
    '''Train model on full data and best hyperparameters
    
    Args:
        imputed_filepath (str): file path to final imputed model data
        seed (int): a seed to set for random_state to preserve reproducibility
        best_lr(float): the best learning rate
        best_numest (int): the best number of estimators
        best_maxd (int): the best max_depth
        best_subsamp (str or list): the best number of sub samples

    Returns:
        trained_model (TMO): trained model object to predict unknowns
    '''
    df = pd.read_csv(imputed_filepath)
    df = one_hot_encode(df)

    predictors = df.loc[:, df.columns != "reviews_per_month_bin"]
    response = df.loc[:, "reviews_per_month_bin"]

    best_gbt = GradientBoostingClassifier(
        learning_rate=best_lr,
        n_estimators=best_numest,
        max_depth=best_maxd,
        subsample=best_subsamp,
        n_iter_no_change=3,
        random_state = seed
    )

    trained_model = best_gbt.fit(predictors,response)
    return trained_model