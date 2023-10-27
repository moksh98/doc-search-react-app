#!/bin/bash
set -xe

# Delete the old directory as needed.
if [ -d /srv/Application/admin ]; then
    rm -rf /srv/Application/admin/
fi

mkdir -vp /srv/Application/admin
