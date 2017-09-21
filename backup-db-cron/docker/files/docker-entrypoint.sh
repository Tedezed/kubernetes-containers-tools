#!/bin/bash
set -e

echo "ver 0.0.0.1"

python /slug-backup-db-cron/main.py subtract_days=$DAYS_TO_DROP

sleep 999