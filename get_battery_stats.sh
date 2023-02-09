#!/usr/bin/env bash

DIR=$PWD
EV_DIR=$(realpath $(dirname ${BASH_SOURCE[0]}))

cd $EV_DIR
source .evBattery_env/bin/activate
source data/.credentials.sh
cd src
python get_battery_stats.py

# --- Back data up
# Local source control
cd $EV_DIR
git checkout data
git add data/car_stats.jsonl
git commit -m "update(data): push updated car stats"

# Github push
# Requires authentication into Github

# Using keychain
KEY="/usr/local/bin/keychain"
if [[ -x $KEY ]]; then
    eval $($KEY --eval --agents "ssh" $HOME/.ssh/github)

# No keychain - use ssh-agent directly
else
    echo "keychain program not found. Might have GH authentication problems"

fi

# Push
git push

# --- Clean-up
# Go back to initial dir
cd $DIR
