#!/bin/bash
set -e

echo "ver 0.0.0.2"

# Drop /etc/crontab
echo > /etc/crontab

if [ $DEV_MODE = "1" ]; then

	python /slug-backup-db-cron/main.py subtract_days=$DAYS_TO_DROP
	echo "Dev mode"
	sleep 999999

fi

printenv | grep -v "TIME" | sed 's/^\(.*\)$/export \1/g' > /root/project_env
chmod +x /root/project_env

echo "$TIME /bin/bash /slug-backup-db-cron/start >> /slug-backup-db-cron/backups/cron.log 2>&1" > /etc/crontab
crontab /etc/crontab

# Start
cron -f

exit 0