#!/bin/bash
set -xe

# Delete the old directory as needed.
if [ -d /srv/Application/frontend ]; then
    rm -rf /srv/Application/frontend/
fi

mkdir -vp /srv/Application/frontend
