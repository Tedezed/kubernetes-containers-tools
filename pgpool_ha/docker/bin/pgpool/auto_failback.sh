#!/bin/bash 

set -x

# Status
#0 - This state is only used during the initialization. PCP will never display it.
#1 - Node is up. No connections yet.
#2 - Node is up. Connections are pooled.
#3 - Node is down.

FILE_KEY_PATH="/var/lib/pgsql/.key_auto_failback"

BACKUP_DIR="/var/lib/pgsql/9.6/backups"
FECHA=$(date +%d-%m-%Y)
BACKUP_TODAY="$BACKUP_DIR/repmgr-$FECHA-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1).tar.gz"

# NEW MASTER
if psql -U $PG_USERNAME -d postgres -c 'SHOW pool_nodes' -w | grep -q "primary" ;
then
	echo "[INFO] Primary node is OK"
	NAME_MASTER_NODE=`psql -U $PG_USERNAME -d postgres -c "SHOW pool_nodes" -w | grep primary | awk '{ print $3 }'`
	ID_NODE_MASTER=`psql -U $PG_USERNAME -d postgres -c "SHOW pool_nodes" -w | grep primary | awk '{ print $1 }'`
	STATUS_MASTER=$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $ID_NODE_MASTER -w | cut -d " " -f 3)
else
	STATUS_MASTER="3"
fi

if (( $STATUS_MASTER == 2 ))
then
	if psql -U $PG_USERNAME -d postgres -c 'SHOW pool_nodes' -w | grep -q "down" ;
	then
		# FAIL NODE
		ID_NODE_FAIL=`psql -U $PG_USERNAME -d postgres -c "SHOW pool_nodes" -w | grep down | awk '{ print $1 }'`
		NAME_NODE_FAIL=`psql -U $PG_USERNAME -d postgres -c "SHOW pool_nodes" -w | grep down | awk '{ print $3 }'`
		STATUS_FAIL=$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $ID_NODE_FAIL -w | cut -d " " -f 3)
	else
		echo "[INFO] Standby node is OK"
		STATUS_FAIL="0"
	fi
	if (( $STATUS_FAIL == 3 ))
	then
		echo "[INFO] Status - Master: $STATUS_MASTER - fail_status: $STATUS_FAIL"
		sleep 5
		if ssh postgres@$NAME_NODE_FAIL "ls $FILE_KEY_PATH" \> /dev/null 2\>\&1;
		then
			echo "--- [WARN] --- Waiting for another process to finish..."
			echo "--- [INFO] --- If this message persists try to delete the file $FILE_KEY_PATH on node $NAME_NODE_FAIL."
			sleep 120
		else
			ssh -T postgres@$NAME_NODE_FAIL "echo $(hostname) > $FILE_KEY_PATH"
			FAILBACK_COMMANDS="
			set -x
			tar -czf $BACKUP_TODAY $PG_DATA_DIRECTORY

			sudo systemctl stop postgresql-9.6.service
			repmgr -f /var/lib/pgsql/repmgr/repmgr.conf -D /var/lib/pgsql/9.6/data -d repmgr -p 5432 -U repmgr -R postgres standby clone $NAME_MASTER_NODE --force
			sudo systemctl start postgresql-9.6.service
			repmgr -f /var/lib/pgsql/repmgr/repmgr.conf -d repmgr -p 5432 -U repmgr -R postgres standby register --force
			"
			echo "--- [WARN] --- NODE $NAME_NODE_FAIL is down - Master node is $NAME_MASTER_NODE"
			STATUS_COMMAND=`ssh -T postgres@$NAME_NODE_FAIL "$FAILBACK_COMMANDS"`
			echo "--- [INFO] --- $STATUS_COMMAND"
			pcp_attach_node -U $PG_USERNAME -p $PCP_PORT -n $ID_NODE_FAIL -w

			echo "--- [INFO] --- End auto_failback..."
			sleep 5
			ssh -T postgres@$NAME_NODE_FAIL "rm $FILE_KEY_PATH"
		fi
	fi
else
	echo "[ERROR] No node master found"
fi
