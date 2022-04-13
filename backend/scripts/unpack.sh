#!/bin/bash

if [ $# -ne 2 ] && [ $# -ne 1 ]
then
  echo "$0 source [destination]"
  exit
fi

ORIG_PWD="$PWD"
SRC="$1"

if [ $# -ne 1 ]
then
  DST="$PWD"
else
  DST="$2"
fi

cd "$DST" || exit
if [ -d "src" ]
then
  if [ -d "src_backup" ]
  then
    rm -rf "src_backup"
  fi
  mv "src" "src_backup"
fi

mkdir "/tmp"
tar zxvf "$SRC" -C "/tmp"

if [ -d "venv" ]
then
  rm -rf "venv"
fi

python3.9 -m venv venv

source venv/bin/activate
pip install /tmp/orgmephi_pack/dependencies/* -f /tmp/orgmephi_pack/dependencies --no-index

cp -r "/tmp/orgmephi_pack/backend" "src"
rm -rf /tmp/orgmephi_pack

if [ ! -f "id_rsa" ] || [ ! -f "id_rsa.pub" ]
then
  ./src/scripts/generate_certs.sh
fi

if [ ! -f "config.py" ]
then
  cp "src/config.py" .
  {
    echo "ORGMEPHI_MEDIA_ROOT_PATH = '$PWD/media'"
    echo "ORGMEPHI_AREA = 'both'"
    echo "ORGMEPHI_PUBLIC_KEY = '$PWD/id_rsa.pub'"
    echo "ORGMEPHI_PRIVATE_KEY = '$PWD/id_rsa'"
  } >> "config.py"
fi

if [ ! -f "orgmephi.ini" ]
then
  cp "src/scripts/orgmephi.ini" .
  sed -i "s,ORGMEPHI_AGGREGATE_CONFIG=.*/config.py,ORGMEPHI_AGGREGATE_CONFIG=$PWD/config.py,g" "orgmephi.ini"
fi

if [ ! -f "run_uwsgi.sh" ]
then
  cp "src/scripts/run_uwsgi.sh" .
  sed -i "s,DIR=.*,DIR=\"$PWD\",g" "run_uwsgi.sh"
fi

cd "$ORIG_PWD" || exit