#!/bin/bash
echo export RCLONE_CONF=${RCLONE_CONF} > /app/set-env
echo export SRC_FILE=${SRC_FILE} >> /app/set-env
echo export TG_TOKEN=${TG_TOKEN} >> /app/set-env
echo export TG_CHANNEL=${TG_CHANNEL} >> /app/set-env

/usr/sbin/crond -c /etc/crontab/ -f
