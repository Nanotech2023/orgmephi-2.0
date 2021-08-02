#!/bin/bash
# run_monolith.sh [port]

scripts/generate_certs.sh
export FLASK_ENV="development"
export FLASK_APP=./aggregate/app.py
export ORGMEPHI_AGGREGATE_CONFIG=./config.py
if [ $# -eq 0 ]
then
  python -m flask run
else
  python -m flask run --port "$1"
fi