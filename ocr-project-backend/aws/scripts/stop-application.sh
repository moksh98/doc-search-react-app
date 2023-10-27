#!/bin/bash
set -x

# Stop application before update
systemctl stop kclds-backend

# Stop celery before update
systemctl stop kclds-celery
