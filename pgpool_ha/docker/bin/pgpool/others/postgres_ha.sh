#!/bin/bash

MODE=$1

CURRENT_DIR="$(echo $0 | sed "s#/postgres_ha.sh##g")"
echo "File: $CURRENT_DIR/set_failover"
source "$CURRENT_DIR/set_failover"

# Install PostgreSQL HA

# For Kubernetes

# mkdir -p /root/templates

# nano /root/templates/master.yaml
# apiVersion: v1
# kind: Service
# metadata:
#   name: postgres-ha-1-1
#   namespace: default
# spec:
#   clusterIP: 10.55.240.101
#   ports:
#   - name: psql
#     port: 5432
#     targetPort: 5432
#     protocol: TCP
#   - name: ssh
#     port: 22
#     targetPort: 22
#     protocol: TCP
# ---
# kind: Endpoints
# apiVersion: v1
# metadata:
#   name: postgres-ha-1-1
#   namespace: default
# subsets:
#   - addresses:
#       - ip: NODE_MASTER_IP
#     ports:
#       - name: psql
#         port: 5432
#       - name: ssh
#         port: 22

# For Nginx

# mkdir -p /etc/nginx/conf-tcp.d
# mkdir -p /etc/nginx/templates

# add to /etc/nginx/nginx.conf
# worker_processes 34;
# events {
#     worker_connections 10;
# }
# include /etc/nginx/conf-tcp.d/*.conf;

# nano /etc/nginx/templates/template-postgres.conf
# stream {
#     upstream backend {
#         server PG_NODE_MASTER:5432;
#     }
#     server {
#         listen 5432;
#         proxy_pass backend;
#     }
# }

# Crontab
#*  *  * * * /bin/bash /root/postgres_ha.sh kubernetes >> /root/postgres_ha.log 2>&1
#*  *  * * * /bin/bash /root/postgres_ha.sh nginx >> /root/postgres_ha.log 2>&1

PG_DATA_DIRECTORY="/var/lib/pgsql/9.6/data"

BACKUP_DIR="/var/lib/pgsql/9.6/backups"
FECHA=$(date +%d-%m-%Y)
BACKUP_TODAY="$BACKUP_DIR/repmgr-$FECHA-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1).tar.gz"

FILE_MASTER="/tmp/old_master"
FILE_KEY="/tmp/postgres_ha_key"

NODES="$PG_PRIMARY_SERVICE_NAME $PG_REPLICA_SERVICE_NAME"
NODE_MASTER_FOUND="3"
NODE_STANBY_FOUND="3"

if [ $MODE = "pgpool_failover" ];
then
	NODE_MASTER_STATUS_PGPOOL="3"
	NODE_STANBY_STATUS_PGPOOL="3"
fi

if [ ! -f $FILE_KEY ]; then

	touch $FILE_KEY

	for n in $NODES;
	do
		# Check node can use command repmgr, repmgr need postgres up
		if ssh postgres@$n "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf cluster show --csv" \> /dev/null 2\>\&1;
		then
			echo "Correct exit in command on node $n"
			repmgr_node_up=$n
		else
			echo "Command failed in $n"
			NODE_FAIL_COMMAND="$n"
		fi
	done

	# Extract data from nodes
	for n in $NODES;
	do
		echo "[INFO] Extract data of node $n ..."
		echo "[INFO] Connect to repmgr in node $repmgr_node_up"
		if ssh postgres@$repmgr_node_up "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf cluster show --csv" \> /dev/null 2\>\&1;
		then
			DIC_NODES=$(ssh postgres@$repmgr_node_up "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf cluster show | grep "^.[0-9]" | sed 's/ //g'")
			INFO_NODE="null|null|null|null"
			for node in $DIC_NODES;
			do
				if [ $(echo "$node" | cut -d "|" -f 2) = "$n" ];
				then
					INFO_NODE="$node"
				fi
			done
			#echo $INFO_NODE
			NODE_ID=$(echo "$INFO_NODE" | cut -d "|" -f 1)
	  		NODE_NAME=$(echo "$INFO_NODE" | cut -d "|" -f 2)
	  		NODE_MODE=$(echo "$INFO_NODE" | cut -d "|" -f 3)
	  		NODE_STATUS=$(echo "$INFO_NODE" | cut -d "|" -f 4)

	  		if [ $NODE_MODE = "primary" ];
	  		then
	  			NODE_MASTER_ID=$NODE_ID
	  			NODE_MASTER_NAME=$NODE_NAME
	  			NODE_MASTER_MODE=$NODE_MODE
	  			NODE_MASTER_STATUS=$NODE_STATUS
	  			if [ "$MODE" = "pgpool_failover" ];
	  			then
	  				for num in {0..1}; do
	  					if [ "$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $num -w | grep -o $NODE_MASTER_NAME)" = "$NODE_MASTER_NAME" ];
	  					then
	  						ID_NODE_MASTER_PGPOOL=$num
	  					fi
	  				done
	  				NODE_MASTER_STATUS_PGPOOL=$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $ID_NODE_MASTER_PGPOOL -w | cut -d " " -f 3)
	  			fi
	  		elif [ $NODE_MODE = "standby" ];
	  		then
	  			NODE_STANBY_ID=$NODE_ID
	  			NODE_STANBY_NAME=$NODE_NAME
	  			NODE_STANBY_MODE=$NODE_MODE
	  			NODE_STANBY_STATUS=$NODE_STATUS
	  			if [ "$MODE" = "pgpool_failover" ];
	  			then
	  				for num in {0..1}; do
	  					if [ "$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $num -w | grep -o $NODE_STANBY_NAME)" = "$NODE_STANBY_NAME" ];
	  					then
	  						ID_NODE_STANBY_PGPOOL=$num
	  					fi
	  				done
	  				NODE_STANBY_STATUS_PGPOOL=$(pcp_node_info -h 127.0.0.1 -U $PG_USERNAME -p $PCP_PORT -n $ID_NODE_STANBY_PGPOOL -w | cut -d " " -f 3)
	  			fi
	  		fi


	  		if [ $NODE_MODE = "primary" ] && [ $NODE_STATUS = "*running" ];
	  		then
	  			echo "Node $NODE_NAME is OK for master"
	  			NODE_MASTER_FOUND="2"
	  		fi
	  		if [ $NODE_MODE = "standby" ] && [ $NODE_STATUS = "running" ];
	  		then
	  			echo "Node $NODE_NAME is OK for stanby"
	  			NODE_STANBY_FOUND="2"
	  		fi
		fi
	done

	echo "MASTER: $NODE_MASTER_ID $NODE_MASTER_NAME $NODE_MASTER_MODE $NODE_MASTER_STATUS"
	echo "STANDBY: $NODE_STANBY_ID $NODE_STANBY_NAME $NODE_STANBY_MODE $NODE_STANBY_STATUS"

	# BEFORE
	if [ "$MODE" = "pgpool_failover" ] || [ "$MODE" = "pgpool_dummy" ];
	then
		echo "[INFO] pgpool before failover"
		pgpool_before $NODE_MASTER_NAME $NODE_STANBY_NAME $MODE $NODE_MASTER_FOUND $NODE_STANBY_FOUND $ID_NODE_MASTER_PGPOOL $ID_NODE_STANBY_PGPOOL
	fi

	################################## PRINCIPAL ##################################
	if [ $NODE_MASTER_FOUND = "2" ] && [ $NODE_STANBY_FOUND = "2" ];
	then
		echo "[PINCIPAL INFO][M: OK | S: OK] Cluster OK"
		set_master $NODE_MASTER_ID $NODE_STANBY_ID $NODE_MASTER_NAME $NODE_STANBY_NAME $MODE $FILE_MASTER
	elif [ $NODE_MASTER_FOUND = "3" ] && [ $NODE_STANBY_FOUND = "3" ];
	then
		echo "[PINCIPAL INFO][M: ER | S: ER] Cluster error"
	elif [ $NODE_MASTER_FOUND = "2" ] && [ $NODE_STANBY_FOUND = "3" ];
	then
		echo "[PINCIPAL INFO][M: OK | S: ER]"
		if [ $PG_DEBUG == "0" ];
		then
			clone_standby $NODE_FAIL_COMMAND $BACKUP_TODAY $PG_DATA_DIRECTORY $NODE_MASTER_NAME
		fi
		set_master $NODE_MASTER_ID $NODE_STANBY_ID $NODE_MASTER_NAME $NODE_STANBY_NAME $MODE $FILE_MASTER
		sleep 2
	elif [ $NODE_MASTER_FOUND = "3" ] && [ $NODE_STANBY_FOUND = "2" ];
	then
		echo "[PINCIPAL INFO][M: ER | S: OK]"
		if [ $PG_DEBUG == "0" ];
		then
			ssh -T postgres@$NODE_STANBY_NAME "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf standby promote"
			ssh -T postgres@$NODE_STANBY_NAME "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf primary unregister --node-id $NODE_MASTER_ID"
			clone_standby $NODE_FAIL_COMMAND $BACKUP_TODAY $PG_DATA_DIRECTORY $NODE_STANBY_NAME
		fi
		sleep 2
	else
		echo "[ERROR] Not found state..."
	fi
	################################## PRINCIPAL ##################################

	if [ $MODE = "pgpool_failover" ] || [ $MODE = "pgpool_dummy" ];
	then
		pgpool_after $NODE_MASTER_NAME $NODE_STANBY_NAME $MODE $NODE_MASTER_FOUND $NODE_STANBY_FOUND $ID_NODE_MASTER_PGPOOL $ID_NODE_STANBY_PGPOOL
	fi

	rm $FILE_KEY
else
	echo "File /tmp/postgres_ha_key found..."
	sleep 10
fi
