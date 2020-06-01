import os
from config import config
import logging
import argparse

from src.train import get_model_data
from src.train import tune_and_score
from src.train import train_model

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
    #configurations
    feature_output_path = config.FEATURE_OUTPUT_LOCATION
    imputed_output_path = config.IMPUTED_OUTPUT_LOCATION
    scores_output_path = config.SCORES_OUTPUT_LOCATION
    seed = config.RANDOM_STATE
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_bucket = config.S3_BUCKET
    s3_path = config.S3_PATH_LOCATION

    parser = argparse.ArgumentParser(description="Train & Predict with the model.")

    #Impute Missing Values
    parser.add_argument('--impute', '-i', default=False, action='store_true',
                            help = "If given, impute missing data and output model-ready data")
    #Option to find best hyperparameters & retrieve CV & Test accuracy
    parser.add_argument('--tune_and_score', '-ts', default=False, action='store_true',
                            help = 'If given, find the best hyperparameters and report CV & Test Accuracy')
    #Option to train full model
    parser.add_argument('--full_model', '-fm', default=False, action='store_true',
                            help = 'If given, train the full model with best hyperparams')


    args = parser.parse_args()

    if args.impute:
        try:
            imputed_df = get_model_data(feature_output_path, seed)
        except Exception:
            logger.error("Something went wrong imputing missing values.")
            raise
        try:
            imputed_df.to_csv(imputed_output_path, index=False)
            logger.info("File: {} created -- imputed values successfully generated".format(imputed_output_path))
        except Exception:
            logger.error("Failed to create imputed.csv")
            raise

    if args.tune_and_score:
        #extract best hyperparameters and scores from test set
        try:
            classifier, cv_auc, cv_acc, test_auc, test_acc = tune_and_score(imputed_output_path, seed, config.TUNING_GRID,
                            config.NUM_ITERS, config.N_JOBS, config.PARAM_SCORING, config.GRID_REFIT, config.TEST_SIZE)
        except Exception:
            logger.error("Something went wrong while tuning and scoring")
            raise

        try:
            with open(scores_output_path, 'w') as f:
                f.write("Best learning_rate: " + str(classifier.best_params_["learning_rate"]) + '\n')
                f.write("Best n_estimators: " + str(classifier.best_params_["n_estimators"]) + '\n')
                f.write("Best max_depth: " + str(classifier.best_params_["max_depth"]) + '\n')
                f.write("Best subsample: " + str(classifier.best_params_["subsample"]) + '\n')
                f.write("CV AUC: " + str(cv_auc) + "\n")
                f.write("CV Accuracy: " + str(cv_acc) + "\n")
                f.write("Test AUC: " + str(test_auc) + "\n")
                f.write("Test Accuracy: " + str(test_acc) + "\n")
                f.close()
            logger.info("File: {} created -- hyperparameters and scoring metrics saved".format(scores_output_path))
        except Exception:
            logger.error("Failed to save hyperparameters and scoring metrics")
            raise

    if args.full_model:
        try:
            trained_model = train_model(imputed_output_path, seed, config.BEST_LR, config.BEST_NUM_EST,
                                config.BEST_MAX_DEPTH, config.BEST_SUBSAMPLE)
            logger.info("Trained model successfully created")
        except Exception:
            logger.error("Trained model was not fit successfully")
            raise
