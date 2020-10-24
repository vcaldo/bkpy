#!/bin/bash
set +
pkill rclone
eval "$(ssh-agent -s)"
ssh-add
/usr/local/bin/python /app/bkpy.py