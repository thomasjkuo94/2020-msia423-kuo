# MSiA 423 Project Charter - Predicting Popular Airbnb Homestays in San Francisco

This application will be developed by Thomas Kuo, with QA support from Catherine Yang.

### Vision:
To increase engagement with the platform, particularly with a focus on increasing successful bookings and stays. 

### Mission:
Using number of reviews as a proxy for the number of stays, understand which features on a listing are primary drivers for the number of reviews a listing receives. This will inform marketplace strategy by building knowledge surrounding what attributes are considered most desirable for a listing. The application will use a Random Forest to classify a listing into 1 of 5 categories based on how many reviews per month they receive. Data will be pulled from [http://insideairbnb.com/get-the-data.html].
An understanding of the features driving a booking decision can stimulate conversations between the company and its host partners to change listing attributes to those that are more likely to be booked.

### Success Criteria:
* Success would be measured by AUC and Accuracy as this is a classification problem that lends itself to these metrics. If at least 70% of the listings are correctly classified into their popularity category, the model can be deemed successful.
* Success would be measured by an increase in listings categorized to bins that are considered "popular", as it implies that those listings are being booked more.

### Outcome:
* Success was measured by AUC and Accuracy: Achieved 0.968 AUC and 86.7% on the Test Set. Success!!

# Backlog

* Initiative 1: Data Preparation and Model Development
  * Epic 1: Understand and Clean Data
    * Story 1: Identify predictors that can be removed from the dataset (medium, complete)
    * Story 2: Check variable types to ensure correctness (medium, complete)
    * Story 3: Change certain formatting (e.g. remove dollar signs) to simplify work (medium, complete)
    * Story 4: Look at predictor and response distribution (medium, complete)
  * Epic 2: Engineer Features
    * Story 1: Impute NAs where sensible (short, complete)
    * Story 2: Bin the response variable based on distribution of bookings per month (short, complete)
  * Epic 3: Develop Model
    * Story 1: Use a baseline of a logistic regression (short, complete)
    * Story 2: Create models using Random Forest, XGBoost, GB tree, and Decision Tree (medium, complete)
    * Story 3: Revise features if necessary based on model AUC and Accuracy (large, complete)

* Initiative 2: Create App Backend
  * Epic 1: Create relational database to store data
    * Story 1: Pipe data to database from website (complete)
    * Story 2: Store data on AWS (complete)
    * Story 3: Test that data fed from database yields same results as offline (complete)

Initiative 3: Create App Frontend
  * Epic 1: Create front page of the app / Flask Development
    * Story 1: Create app input, select certain features to drive model (complete)
    * Story 2: Display Model Output (complete)



# MSiA423 Template Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Set up environment variables](#1-set-up-environment-variables)
  * [2. Build the image](#2-build-the-image)
  * [3. Push data to S3](#3-push-data-to-s3)
  * [4. Model pipeline](#4-model-pipeline)
  * [5. Running test scripts](#5-running-test-scripts)
  * [6. Running web app](#6-running-web-app)
  * [7. Running MySql](#7-running-mysql)
  
<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── Dockerfile                    <- Dockerfile for building image to run model training pipeline + testing
│   ├── Dockerfile_app                <- Dockerfile for building image to run app
│   ├── boot.sh                       <- bash script used by Dockerfile_app to execute flaskapp
│   ├── boot_test.sh                  <- bash script used Dockerfile to execute pytest
│   ├── boot_train.sh                 <- bash script used Dockerfile to execute model training pipeline
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API
│   ├── config.py                     <- Configurations for local data storage & S3 bucket location
│   ├── CHANGEME.env                  <- Rename "config.env" if desired; Please enter S3 Access Keys & RDS Host,Port,User,Password,DB
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│   ├── mybnb.pdf                     <- final presentation slides in pdf format

│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project
│   ├── ingestion.py                  <- Python Module imported by run_s3.py to help with ingestion
│   ├── downloads3.py                 <- Python Module imported by run_cleanandfeat.py to download raw data from S3
│   ├── clean.py                      <- Python Module imported by run_cleanandfeat.py to clean raw data
│   ├── create_features.py            <- Python Module imported by run_cleanandfeat.py to create features
│   ├── train.py                      <- Python Module imported by run_model.py to impute, tune hyperparameters, save TMOs
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run_s3.py                         <- Simplifies the execution of ingesting data & pushing to S3 
├── run_database.py                   <- Simplifies the execution of creating db locally or in rds
├── run_cleanandfeat.py               <- Simplifies the execution of downloading, cleaning, and creating features
├── run_model.py                      <- Simplifies the execution of imputing, hyperparameter turning, and model training
├── test_airbnb.py                    <- Simplifies the execution of testing
├── requirements.txt                  <- Python package dependencies 
```
## Running the app in Docker 

### 1. Set up environment variables

The config files for running the flask app are in the `config/` folder. 
CHANGEME.env needs to be renamed to config.env and it includes a place to store S3 Access Keys and RDS Host,User,Password,Port,and db information.\
config.py includes variables to configure local data storage, as well as S3 bucket information\
flaskconfig.py includes configurations for flask app, including local and RDS MYSQL databases.

Step A discusses how to use a .env file to set environmnent variables.\
Step B discusses how to set them using command line.

a) CHANGEME.env specifics (from ROOT):
```bash
vi config/CHANGEME.env
```

Fill in for S3 bucket:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY 

Fill in for AWS RDS instance:
* MYSQL_HOST
* MYSQL_PORT
* MYSQL_USER
* MYSQL_PASSWORD
* MYSQL_DATABASE

b) : It is not necessarily to rename CHANGEME.env to config.env as discussed in step A. The same environment variables can be passed in directly through the command line for each docker run using the -e or --env-file flags.

### 2. Build the image 

The Dockerfiles for running both the model training and flask app are in the `app/` folder.\
To build the image for the model training/testing, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t airbnb .
```

This command builds the Docker image for model training, with the tag `airbnb`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

To build the image for the webapp, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile_app -t airbnb_webapp .
```

This command builds the Docker image for webapp, with the tag `airbnb_webapp`, based on the instructions in `app/Dockerfile_app` and the files existing in this directory.
 
### 3. Push data to S3

To push data to S3, run from this directory: 

```bash
docker run -e AWS_ACCESS_KEY_ID=<KEY> -e AWS_SECRET_ACCESS_KEY=<SECRET KEY> --mount type=bind,source=$(pwd)/data,target=/app/data airbnb run_s3.py
```

This command runs the `run_s3.py` command in the `airbnb` image to push source data into S3.
`--mount type=bind,source=$(pwd)/data,target=/app/data` mounts the source data so it persists in `data/`


### 4. Model pipeline

The model training pipeline uses the `boot_train.sh` script to execute `run_cleanandfeat.py` and `run_model.py`:\
run_cleanandfeat.py has the following arguments:
* `--download` or `-d`, which downloads from the S3 bucket into local
* `--clean` or `-c`, which cleans the downloaded data
* `--featurize` or `-f`, which creates features from cleaned data

run_model.py has the following arguments:
* `--impute` or `-i`, which imputes missing values from the cleaned & featurized data
* `--tune_and_score` or `-ts`, which tunes the hyperparameters and outputs cross-validation & test AUC & Accuracy
* `--full_model` or `-fm`, which trains the model on the full data set tuned with the hyperparameters and returns a trained model object and encoder for prediction

The pipeline runs in the order the arguments are listed, and by default `boot_train.sh` provides all of those arguments to the two scripts. Users can open the `.sh` to remove an argument if they so desire.

Running Model Pipeline:
```bash
docker run -e AWS_ACCESS_KEY_ID=<KEY> -e AWS_SECRET_ACCESS_KEY=<SECRET KEY> --mount type=bind,source=$(pwd)/data,target=/app/data airbnb app/boot_train.sh
```

This command runs `app/boot_train.sh` command in the `airbnb` image to execute the end-to-end model pipeline\.
*Note, that as before the data needs to be mounted in order to persist the database in the local data folder.


### 5. Running test scripts

Use the same image created for the model pipeline for test scripts. The test script uses the `app/boot_test.sh` and pytest to execute the `test_airbnb.py` located in the root directory.

Execute the `test_airbnb.py` as follows:
```bash
docker run airbnb app/boot_test.sh
```

### 6. Running web app

This assumes you have already built the docker image `airbnb_webapp` as described in step 2. The webbapp uses the `app/boot.sh` to execute the `run_database.py` and `app.py`, both located in the root directory.\
run_database.py has the following arguments:
* `--truncate` or `-t`, which deletes existing observations from the local sqlite database or AWS RDS.\
app.py has no arguments, and executes the flaskapp.

There are two ways to execute the web app:
a) Local database connection
```bash
docker run --mount type=bind,source=$(pwd)/data,target=/app/data -p 5000:5000 --name test airbnb_webapp
```
b) AWS RDS database connection (you can also supply a SQLALCHEMY_DATABASE_URI directly as an environment variable)
```bash
docker run --env-file=config/config.env --mount type=bind,source=$(pwd)/data,target=/app/data -p 5000:5000 --name test airbnb_webapp
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the airbnb_webapp image as a container named test and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port.

If PORT in config/flaskconfig.py is changed, this port should be changed accordingly (as should the EXPOSE 5000 line in app/Dockerfile_app)

### 7. Running MySql

Once an RDS table is created, you can run the MySql client to access it. If you haven't already, you must create a mysql config file at root using the command `vi .mysqlconfig`. You should set MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD variables to be the same as how they were set in `config/config.env`.

After this is complete, set your environment variables in ~/.bashrc
```bash
echo 'source .mysqlconfig' >> ~/.bashrc
source ~/.bashrc
```

You should now be able to run the command below:
```bash
docker run -it --rm mysql:latest mysql -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PASSWORD}
```

The command above enables to make a connection to the RDS instance where the table is hosted.
Specifically for this use case, access the `msia423_db` database and use the sql command `show columns in abb_feat_and_resp;` to ensure that the columns have been created.

