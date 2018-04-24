#! /bin/sh -x

# Executes this command after master failover
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
log="/tmp/follow_master.log"

echo "[FAILBACK] $datetime" >> $log
echo "$1 $2 $3 $4" >> $log