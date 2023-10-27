#!/bin/bash
set -x

# Start celery after update
systemctl start kclds-celery

# Start application after update
systemctl start kclds-backend
