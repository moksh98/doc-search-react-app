#!/bin/bash
set -xe

# Delete the old directory as needed.
if [ -d /srv/Application/backend ]; then
    rm -rf /srv/Application/backend/
fi

mkdir -vp /srv/Application/backend
