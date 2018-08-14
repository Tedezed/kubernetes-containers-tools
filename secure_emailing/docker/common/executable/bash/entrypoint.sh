#!/bin/bash
set -e

# Config database
sed -i -e "s/{{DB_HOST}}/$DB_HOST/g" /mnt/common/smtp_proxy_v2/emailing.conf
sed -i -e "s/{{DB_NAME}}/$DB_NAME/g" /mnt/common/smtp_proxy_v2/emailing.conf
sed -i -e "s/{{DB_USER}}/$DB_USER/g" /mnt/common/smtp_proxy_v2/emailing.conf
sed -i -e "s/{{DB_PASSWORD}}/$PGPASSWORD/g" /mnt/common/smtp_proxy_v2/emailing.conf

if [ "$DEBUG" == "True" ]; then
	sleep infinity
fi

# Check database server
while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} > /dev/null 2> /dev/null; do
	echo "Connecting to ${DB_HOST} Failed..."
	sleep 5
done
echo "Connecting to ${DB_HOST}..."

# Check database
if [ "$DB_NAME" != 'postgres' ]; then
	if psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
		echo "Database $DB_NAME exists"
	else
		echo "Create database $DB_NAME"
		psql -U $DB_USER -h $DB_HOST -p $DB_PORT -a -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
		psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT < /mnt/common/smtp_proxy_v2/sql/database.sql
	fi
fi

# Run server Python
echo "Run Securemail"
python /mnt/common/smtp_proxy_v2/mail_relay.py --localport $PORT --remotehost $REMOTE_HOST --remoteport $REMOTE_PORT