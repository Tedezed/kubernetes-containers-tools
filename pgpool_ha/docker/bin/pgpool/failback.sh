#! /bin/sh

LOG_FILE="/tmp/failback.log"
echo "Run FAILBACK" >> /tmp/failback.log

# Executes this command at failback.
# Special values:
#   %d = node id
#   %h = host name
#   %p = port number
#   %D = database cluster path
#   %m = new master node id
#   %H = hostname of the new master node
#   %M = old master node id
#   %P = old primary node id
#   %r = new master port number
#   %R = new master database cluster path
#   %% = '%' character

pghome=$PG_HOME
pgdata=$PG_DATA_DIRECTORY

#echo "$1 $2 $3 $4" >> $LOG_FILE

#./recovery_1st_stage $pgdata 10.63.250.111 /var/lib/pgsql/9.6/data 5432
