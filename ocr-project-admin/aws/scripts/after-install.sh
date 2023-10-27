#!/bin/bash
set -xe

# Copy environment file
cp /srv/Application/admin.env /srv/Application/admin/.env

# Ensure the ownership permissions are correct.
chown -hR ubuntu:ubuntu /srv/Application/admin
