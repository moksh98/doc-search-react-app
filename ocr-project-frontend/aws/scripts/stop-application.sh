#!/bin/bash
set -x

# Stop application for update
sudo -u ubuntu pm2 stop "Front End"
