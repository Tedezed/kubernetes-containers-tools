#! /bin/sh -x
# Execute command by failover.
# special values:  %d = node id
#                  %h = host name
#                  %p = port number
#                  %D = database cluster path
#                  %m = new master node id
#                  %M = old master node id
#                  %H = new master node host name
#                  %P = old primary node id
#                  %R = new master database cluster path
#                  %r = new master port number
#                  %% = '%' character

falling_node=$1          # %d
old_primary=$2           # %P
new_primary=$3           # %H
pgdata=$4                # %R

pghome=/usr/pgsql-9.6
log=/var/log/pgpool/failover.log

date >> $log
echo "failed_node_id=$falling_node new_primary=$new_primary" >> $log

if [ $falling_node = $old_primary ]; then
    if [ $UID -eq 0 ]
    then
        su postgres -c "ssh -T postgres@$new_primary $pghome/bin/pg_ctl promote -D $pgdata"
    else
        ssh -T postgres@$new_primary $pghome/bin/pg_ctl promote -D $pgdata
    fi
    exit 0;
fi;
exit 0;