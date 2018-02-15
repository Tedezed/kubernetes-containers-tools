#!/bin/bash

cp /files/conf/pgbouncer.ini $CONFDIR

sed -i "s/PG_SERVICE_NAME/$PG_SERVICE_NAME/g" $CONFDIR/pgbouncer.ini
sed -i "s/DB_NAME/$DB_NAME/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_SERVICE_PORT/$PG_SERVICE_PORT/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_ADMIN/$PG_ADMIN/g" $CONFDIR/pgbouncer.ini
sed -i "s/PG_PORT/$PG_PORT/g" $CONFDIR/pgbouncer.ini

pgbouncer $CONFDIR/pgbouncer.ini -R &

wait