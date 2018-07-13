#!/bin/bash

set -x
export
cp /files/conf/pgbouncer.ini $CONFDIR

sed -i "s/PG_SERVICE_NAME/$PG_SERVICE_NAME/g" $CONFDIR/pgbouncer.ini
sed -i "s/DB_NAME/$DB_NAME/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_SERVICE_PORT/$PG_SERVICE_PORT/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_ADMIN/$PG_ADMIN/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_PORT/$PG_PORT/g" $CONFDIR/pgbouncer.ini

sed -i "s/POOL_MODE/$POOL_MODE/g" $CONFDIR/pgbouncer.ini
sed -i "s/MAX_CON/$MAX_CON/g" $CONFDIR/pgbouncer.ini
sed -i "s/DEFAULT_POOL_SIZE/$DEFAULT_POOL_SIZE/g" $CONFDIR/pgbouncer.ini
sed -i "s/MIN_POOL_SIZE/$MIN_POOL_SIZE/g" $CONFDIR/pgbouncer.ini

sed -i "s/CONFDIR/$DIR_CONFDIR/g" $CONFDIR/pgbouncer.ini
encrypted_pass="md5$(echo -n "$PG_PASSWORD$PG_USERNAME" | md5sum | cut -f 1 -d ' ')"
echo "\"$PG_USERNAME\" \"$encrypted_pass\"" >> ${CONFDIR}/userlist.txt
echo "Wrote authentication credentials to ${CONFDIR}/userlist.txt"

pgbouncer $CONFDIR/pgbouncer.ini -R &

wait