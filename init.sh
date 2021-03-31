#!/usr/bin/env bash

source "/home/pi/export_vars.sh"
cd /home/pi/rpi-rgb-led-matrix/bindings/python/samples

# Start the Spotify LED Script
sudo -E python3 spotify.py --led-cols 64 -b 10 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start /home/pi/rpi-rgb-led-matrix/bindings/python/samples/spotify.py : $status"
  exit $status
fi
# Naive check runs checks once a minute to see if either of the processes exited.

while sleep 60; do
  ps aux |grep "sudo -E python3 spotify.py --led-cols 64 -b 10" |grep -q -v grep
  PROCESS_1_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi