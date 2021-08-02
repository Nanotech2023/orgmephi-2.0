#!/bin/bash
# run_microservice.sh [analytics port] [contest port] [user port]

scripts/generate_certs.sh
if [ $# -eq 0 ]
then
  APORT=5000
else
  APORT=$1
fi

if [ $# -le 1 ]
then
  CPORT=$((APORT + 1))
else
  CPORT=$2
fi

if [ $# -le 2 ]
then
  UPORT=$((CPORT + 1))
else
  UPORT=$3
fi

export FLASK_ENV="development"
export ORGMEPHI_ANALYTICS_CONFIG=./config.py
export ORGMEPHI_CONTEST_CONFIG=./config.py
export ORGMEPHI_USER_CONFIG=./config.py

trap '' 2

echo "Running analytics services on port $APORT"
FLASK_APP=./analytics/app.py python -m flask run --port "$APORT" >> analytics.log 2>&1 &
ANALYTICS_PID=$!

echo "Running contest services on port $CPORT"
FLASK_APP=./contest/app.py python -m flask run --port "$CPORT" >> contest.log 2>&1 &
CONTEST_PID=$!

echo "Running user services on port $UPORT"
FLASK_APP=./user/app.py python -m flask run --port "$UPORT" >> user.log 2>&1 &
USER_PID=$!

echo "Press enter to end all services"
read

kill $ANALYTICS_PID
kill $CONTEST_PID
kill $USER_PID

trap 2