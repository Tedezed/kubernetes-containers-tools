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

#pghome=/usr/pgsql-9.6
#log=/var/log/pgpool/failover.log

pghome=$PG_HOME
log=$LOG_FAILOVER
falling_node=$1          # %d
old_primary=$2           # %P
new_primary=$3           # %H
pgdata=$4                # %R

date >> $log
echo "failed_node_id=$falling_node old_primary=$old_primary new_primary=$new_primary pgdata=$pgdata pghome=$pghome" >> $log

if [ -z "$old_primary" ] || [ -z "$new_primary" ];
then
	echo "[WARNING] No execute failover..." >> $log
else
	echo "[INFO] Execute failover (L)" >> $log
	if [ $falling_node = $old_primary ];
	then
	    if [ $UID -eq 0 ]
	    then
	    	echo "UID: $UID"
	        su postgres -c "ssh -T postgres@$new_primary /usr/pgsql-9.6/bin/pg_ctl promote -D $pgdata"
	    else
	    	echo "UID: $UID"
	        ssh -T postgres@$new_primary /usr/pgsql-9.6/bin/pg_ctl promote -D $pgdata
	    fi
	    exit 0;
	fi;
fi;
exit 0;
