#!/bin/bash
set -x
pkill rclone
pkill python
pkill ssh-agent
eval "$(ssh-agent -s)"
ssh-add
/usr/local/bin/python /app/bkpy.py