#!/usr/bin/env bash

#python3 run_flask.py create_db
#python3 run_flask.py ingest
python3 run_database.py -t
python3 app.py