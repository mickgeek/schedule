#!/bin/sh
set -e

if [ "$1" = 'node' ]; then
    cd ./client/

    npm install --location=global @angular/cli
    npm install
    npm run start
fi

exec "$@"
