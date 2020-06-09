import os
from config import config
import logging
import argparse
import pickle

from src.train import get_model_data
from src.train import tune_and_score
from src.train import train_model

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
    
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

    #feature output filepath
    parser.add_argument('--feature_path', '-fp', default=config.FEATURE_OUTPUT_LOCATION,
                            help = "If given, create filepath for feature data")
    #imputed output filepath
    parser.add_argument('--imputed_path', '-ip', default=config.IMPUTED_OUTPUT_LOCATION,
                            help = "If given, change filepath for imputed data")
    #scoring metrics output filepath
    parser.add_argument('--scores_path', '-sp', default=config.SCORES_OUTPUT_LOCATION,
                            help = "If given, change filepath for scoring metrics")
    #trained model output filepath
    parser.add_argument('--model_path', '-mp', default=config.SAVED_MODEL_LOCATION,
                            help = "If given, change filepath for scoring metrics")
    #encoder output filepath
    parser.add_argument('--encoder_path', '-ep', default=config.SAVED_ENCODER_LOCATION,
                            help = "If given, change filepath for scoring metrics")

    args = parser.parse_args()

    if args.impute:
        try:
            imputed_df = get_model_data(args.feature_path, config.RANDOM_STATE)
        except Exception:
            logger.error("Something went wrong imputing missing values.")
            raise
        try:
            imputed_df.to_csv(args.imputed_path, index=False)
            logger.info("File: {} created -- imputed values successfully generated".format(args.imputed_path))
        except Exception:
            logger.error("Failed to create imputed.csv")
            raise

    if args.tune_and_score:
        #extract best hyperparameters and scores from test set
        try:
            classifier, cv_auc, cv_acc, test_auc, test_acc = tune_and_score(args.imputed_path, config.RANDOM_STATE, config.TUNING_GRID,
                            config.NUM_ITERS, config.N_JOBS, config.PARAM_SCORING, config.GRID_REFIT, config.TEST_SIZE)
        except Exception:
            logger.error("Something went wrong while tuning and scoring")
            raise

        try:
            with open(args.scores_path, 'w') as f:
                f.write("Best learning_rate: " + str(classifier.best_params_["learning_rate"]) + '\n')
                f.write("Best n_estimators: " + str(classifier.best_params_["n_estimators"]) + '\n')
                f.write("Best max_depth: " + str(classifier.best_params_["max_depth"]) + '\n')
                f.write("Best subsample: " + str(classifier.best_params_["subsample"]) + '\n')
                f.write("CV AUC: " + str(cv_auc) + "\n")
                f.write("CV Accuracy: " + str(cv_acc) + "\n")
                f.write("Test AUC: " + str(test_auc) + "\n")
                f.write("Test Accuracy: " + str(test_acc) + "\n")
                f.close()
            logger.info("File: {} created -- hyperparameters and scoring metrics saved".format(args.scores_path))
        except Exception:
            logger.error("Failed to save hyperparameters and scoring metrics")
            raise

    if args.full_model:
        try:
            trained_model = train_model(args.imputed_path, config.RANDOM_STATE, config.BEST_LR, config.BEST_NUM_EST,
                                config.BEST_MAX_DEPTH, config.BEST_SUBSAMPLE, args.encoder_path)
            pickle.dump(trained_model, open(args.model_path, "wb"))
            logger.info("Trained model successfully created")
        except Exception:
            logger.error("Trained model was not fit successfully")
            raise
