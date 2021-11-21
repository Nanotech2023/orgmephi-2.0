#!/bin/bash

DIR="$PWD"
cd "$DIR" || exit

start() {
  if [ -f "/tmp/orgmephi_pid.txt" ]
  then
    echo "Already running"
    return
  fi
  source venv/bin/activate
  nohup uwsgi --ini orgmephi.ini --uid www-data --gid www-data >/dev/null 2>&1 &
  echo $! > /tmp/orgmephi_pid.txt
}

stop() {
  if [ ! -f "/tmp/orgmephi_pid.txt" ]
  then
    echo "Not running"
    return
  fi
  kill "$(cat "/tmp/orgmephi_pid.txt")"
  rm "/tmp/orgmephi_pid.txt"
}

restart() {
  if [ -f "/tmp/orgmephi_pid.txt" ]
  then
    kill "$(cat "/tmp/orgmephi_pid.txt")"
    rm "/tmp/orgmephi_pid.txt"
    sleep 5
  fi
  source venv/bin/activate
  nohup uwsgi --ini orgmephi.ini --uid www-data --gid www-data >/dev/null 2>&1 &
  echo $! > /tmp/orgmephi_pid.txt
}

case $1 in
  start|stop|restart) "$1" ;;
esac
