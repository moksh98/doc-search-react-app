#!/bin/bash
set -xe

# Use Pip to update/install Python requirements
sudo -u ubuntu /home/ubuntu/.local/bin/pip3 install -r /srv/Application/backend/requirements.txt

# Copy environment file
cp /srv/Application/backend.env /srv/Application/backend/.env

# Ensure the ownership permissions are correct.
chown -hR ubuntu:ubuntu /srv/Application/backend

if [ ! -d "/home/ubuntu/images" ]; then
    mkdir /home/ubuntu/images
    chown -hR ubuntu:ubuntu /home/ubuntu/images
fi
if [ ! -d "/home/ubuntu/input_pdfs" ]; then
    mkdir /home/ubuntu/input_pdfs
    chown -hR ubuntu:ubuntu /home/ubuntu/input_pdfs
fi
if [ ! -d "/home/ubuntu/output_pdfs" ]; then
    mkdir /home/ubuntu/output_pdfs
    chown -hR ubuntu:ubuntu /home/ubuntu/output_pdfs
fi

# Setup alembic migration to ensure database is up-to-date with new fields
cd /srv/Application/backend
sudo -u ubuntu /home/ubuntu/.local/bin/alembic upgrade head