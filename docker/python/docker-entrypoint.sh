#!/bin/sh
set -e

if [ "$1" = 'python' ]; then
    cd ./server/

    python -m venv ./venv/
    source ./venv/bin/activate

    pip install --upgrade pip
    pip install --requirement ./requirements.txt
fi

exec "$@" ./src/app.py
