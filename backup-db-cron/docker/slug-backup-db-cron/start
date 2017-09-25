#!/bin/bash

source /root/project_env

printenv > /slug-backup-db-cron/backups/cronenv

/usr/bin/python /slug-backup-db-cron/main.py subtract_days=30