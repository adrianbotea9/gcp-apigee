#!/bin/bash
set -e

#check if the json file exists
if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "Credentials file does not exist"
    exit 1
fi

exec python gcp/apigee-apps.py "$@"
