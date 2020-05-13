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

# Backlog

* Initiative 1: Data Preparation and Model Development
  * Epic 1: Understand and Clean Data
    * Story 1: Identify predictors that can be removed from the dataset (medium, planned)
    * Story 2: Check variable types to ensure correctness (medium, planned)
    * Story 3: Change certain formatting (e.g. remove dollar signs) to simplify work (medium, planned)
    * Story 4: Look at predictor and response distribution (medium, planned)
  * Epic 2: Engineer Features
    * Story 1: Impute NAs where sensible (short, planned)
    * Story 2: Bin the response variable based on distribution of bookings per month (short, planned)
  * Epic 3: Develop Model
    * Story 1: Use a baseline of a logistic regression (short, planned)
    * Story 2: Create models using Random Forest, XGBoost, GB tree, and Decision Tree (medium, planned)
    * Story 3: Revise features if necessary based on model AUC and Accuracy (large, planned)

* Initiative 2: Create App Backend
  * Epic 1: Create relational database to store data
    * Story 1: Pipe data to database from website (icebox)
    * Story 2: Store data on AWS (icebox)
    * Story 3: Test that data fed from database yields same results as offline (icebox)

Initiative 3: Create App Frontend
  * Epic 1: Create front page of the app / Flask Development
    * Story 1: Create app input, select certain features to drive model (icebox)
    * Story 2: Display Model Output (icebox)



# MSiA423 Template Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Set up config files](#1-set-up-config-files)
  * [2. Build the image](#2-build-the-image)
  * [3. Push data to S3](#3-push-data-to-s3)
  * [4. Configurable database creation](#4-configurable-database-creation)
  * [5. Running MySql](#5-running-mysql)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│    ├── flaskconfig.py                <- Configurations for Flask API
│    ├── config.py                    <- Configurations for local data storage & S3 bucket location
│    ├── CHANGEME.env                 <- Rename "config.env"; Please enter S3 Access Keys & RDS Host,Port,User,Password,DB
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
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
│   ├── helpers.py                    <- Python Module imported by run_database.py to help with db creation
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run_s3.py                         <- Simplifies the execution of ingesting data & pushing to S3 
├── run_database.py                   <- Simplifies the execution of creating db locally or in rds
├── requirements.txt                  <- Python package dependencies 
```
## Running the app in Docker 

### 1. Set up config files

The config files for running the flask app are in the `config/` folder. 
CHANGEME.env needs to be renamed to config.env and it includes a place to store S3 Access Keys and RDS Host,User,Password,Port,and db information.
config.py includes variables to configure local data storage, as well as S3 bucket information

a) CHANGEME.env specifics (from ROOT):
```bash
vi config/CHANGEME.env
```

Fill in AWS_ACCESS_KEY, SECRET_ACCESS_KEY for your S3 bucket. Also, fill MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, DATABASE_NAME with the credentials related to the AWS RDS instance you want to access.

b) config.py specifics (from ROOT):
```bash
vi config/config.py
```

Local database information is stored here, you may change if needed to but default local databases will persist in the `data/` folder.
S3 configurations are stored as well. No need to change SOURCE_DATA_URL as that is our raw source. AIRBNB_RAW_LOCATION by default stores the source data in the `data/` folder. S3_BUCKET refers to the S3 bucket for the source data to be uploaded to, while S3_PATH_LOCATION refers to where the source data will be pushed.

### 2. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t airbnb .
```

This command builds the Docker image, with the tag `airbnb`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 3. Push data to S3

To push data to S3, run from this directory: 

```bash
docker run --env-file=config/config.env --mount type=bind,source=$(pwd)/data,target=/app/data airbnb run_s3.py
```

This command runs the `run_s3.py` command in the `airbnb` image to push source data into S3.
`--env-file=config/config/env` feeds the environment variables
`--mount type=bind,source=“$(pwd)“/data,target=/app/data` mounts the source data so it persists in `data/`


### 4. Configurable database creation

There are two ways to create the database, by configuration.
--local` or `-l` flags can be used to push the database locally, while `--rds` or `-r` flags can be used to push the database to RDS.

Local Database:
```bash
docker run --env-file=config/config.env --mount type=bind,source=$(pwd)/data,target=/app/data airbnb run_database.py --local
```

This command runs `run_database.py` command in the `airbnb` image to create a database locally.
*Note, that as before the data needs to be mounted in order to persist the database in the db folder.

RDS Database:
```bash
docker run --env-file=config/config.env airbnb run_database.py --rds
```

This command runs `run_database.py` command in the `airbnb` image to create a table in rds.

### 5. Running MySql

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
Specifically for this use case, access the `msia423_db` database and use the sql command `show columns in abb_feat_and_resp;` to ensure that the columns have been created. There is no data in the table at this point 5/12/2020.

