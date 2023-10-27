#!/bin/bash
set -xe

# Copy environment file
cp /srv/Application/frontend.env /srv/Application/frontend/.env

# Ensure the ownership permissions are correct.
chown -hR ubuntu:ubuntu /srv/Application/frontend
