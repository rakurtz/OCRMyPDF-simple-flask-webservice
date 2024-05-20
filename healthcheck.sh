#!/bin/bash
# simple healthcheck script to determine if we are still alive
if pgrep -f main.py > /dev/null
then
  exit 0
else
  exit 1
fi
