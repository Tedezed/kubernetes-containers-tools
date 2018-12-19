#!/bin/bash

set -e
echo "v0.1"
echo "User: $(whoami)"
echo "Start backup - $(date)"

# Backup code

cd /kubernetes-resources/kubebackup/
bash kubebackup_v1.bash

DATE_NOW=$(date +%d-%m-%Y)
DROP_DATE=$(date +%d-%m-%Y --date="$DAYS days ago")

mkdir -p /root/backups/$DATE_NOW
mv /kubernetes-resources/kubebackup/bkp/* /root/backups/$DATE_NOW
find /root/backups/* -maxdepth 0 -mtime "+$DAYS" -type d -exec rm -rf {} \;

# Backup code

echo "End backup - $(date)"
