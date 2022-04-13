#!/bin/bash

ORIG_PWD="$PWD"
cd "$(dirname "$0")/../.." || exit

mkdir /tmp/orgmephi_pack
cp -r backend /tmp/orgmephi_pack
python3.9 -m pip download -r backend/requirements.txt -d "/tmp/orgmephi_pack/dependencies"
cd "/tmp" || exit
tar cvfz "orgmephi_pack.tar.gz" "orgmephi_pack"
cd "$ORIG_PWD" || exit
mv "/tmp/orgmephi_pack.tar.gz" .
rm -rf "/tmp/orgmephi_pack"