#!/bin/bash
set -x

# Start application after update
sudo -u ubuntu pm2 start "Front End"
