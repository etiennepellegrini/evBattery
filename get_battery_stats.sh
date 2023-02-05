#!/usr/bin/env bash

DIR=$PWD
WD=$(dirname ${BASH_SOURCE[0]})

source $WD/.evBattery_env/bin/activate
source $WD/data/.credentials.sh
cd $WD/src
python get_battery_stats.py

# Back data up on Github
git checkout data
git add data/car_stats.jsonl
git commit -m "update(data): push updated car stats"
git push

# Go back to initial dir
cd $DIR
