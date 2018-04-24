#!/bin/bash
# first stage recovery
# $1 datadir
# $2 desthost
# $3 destdir

# pgdata=$1
# remote_host=$2
# remote_pgdata=$3
# port=$4

BACKUP_DIR="/var/lib/pgsql/9.6/backups/"
FECHA=$(date +%d-%m-%Y)
BACKUP_DIR_TODAY="repmgr-$BACKUP_DIR$FECHA-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)/"

#as I'm using repmgr it's not necessary for me to know datadir(master) $1
RECOVERY_NODE=$2
CLUSTER_PATH=$3
#repmgr needs to know the master's ip
#MASTERNODE=`/sbin/ifconfig eth0 | grep inet | awk '{print $2}' | sed 's/addr://'`
MASTERNODE=$(hostname)

pg_basebackup -h $MASTERNODE -U repl -D $CLUSTER_PATH -x -c fast

cmd1=`ssh postgres@$RECOVERY_NODE "repmgr -D $CLUSTER_PATH --force standby clone $MASTERNODE"`
echo $cmd1 >> /tmp/repmgr-basebackup.log