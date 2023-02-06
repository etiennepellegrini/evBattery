#!/usr/bin/env bash

DIR=$PWD
EV_DIR=$(dirname ${BASH_SOURCE[0]})

cd $EV_DIR
source .evBattery_env/bin/activate
source data/.credentials.sh
cd src
python get_battery_stats.py

# Back data up on Github
cd $EV_DIR
git checkout data
git add data/car_stats.jsonl
git commit -m "update(data): push updated car stats"
git push

# Go back to initial dir
cd $DIR
