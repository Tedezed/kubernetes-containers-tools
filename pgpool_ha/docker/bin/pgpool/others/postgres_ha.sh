#!/bin/bash

MODE=$1

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

FILE_MASTER="/root/old_master"
FILE_KEY="/tmp/postgres_ha_key"

NODES="pg1 pg2"
NODE_MASTER_FOUND="3"
NODE_STANBY_FOUND="3"

function reload_stream {
	
	NODE_MASTER_NAME=$1
	FILE_MASTER=$2

	if [ -e $FILE_MASTER ]
	then
		if [ $(cat "$FILE_MASTER") = "$NODE_MASTER_NAME" ];
		then
			RELOAD="0"
			echo "Master update OK: no reload"
		else
			RELOAD="1"
		fi
	else
		RELOAD="1"
	fi

	if [ $RELOAD = "1" ];
	then
		echo "New master: reload"
		bash -c "echo $NODE_MASTER_NAME > $FILE_MASTER"
		
		# Kubernetes
		if [ $MODE = "kubernetes" ];
		then
			echo "Reload conf Kubernetes..."
			cp /root/templates/master.yaml /root/master.yaml
			sed -i "s/NODE_MASTER_IP/$(getent hosts $NODE_MASTER_NAME | awk '{ print $1 }')/g" /root/master.yaml
			kubectl delete -f /root/master.yaml
			kubectl create -f /root/master.yaml
		# Nginx
		elif [ $MODE = "nginx" ];
		then
			echo "Reload Nginx..."
			cp /etc/nginx/templates/template-postgres.conf /etc/nginx/conf-tcp.d/postgres.conf
			sed -i "s/PG_NODE_MASTER/$NODE_MASTER_NAME/g" /etc/nginx/conf-tcp.d/postgres.conf
			systemctl reload nginx.service
		fi
	fi
}

if [ ! -f $FILE_KEY ]; then

	touch $FILE_KEY

	for n in $NODES;
	do
		echo "Connect to $n"
		if ssh postgres@$n "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf cluster show --csv" \> /dev/null 2\>\&1;
		then
			DIC_NODES=$(ssh postgres@$n "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf cluster show | grep "^.[0-9]" | sed 's/ //g'")
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
	  		elif [ $NODE_MODE = "standby" ];
	  		then
	  			NODE_STANBY_ID=$NODE_ID
	  			NODE_STANBY_NAME=$NODE_NAME
	  			NODE_STANBY_MODE=$NODE_MODE
	  			NODE_STANBY_STATUS=$NODE_STATUS
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
		else
			echo "Command failed in $n"
			NODE_FAIL_COMMAND="$n"
		fi
	done

	if [ $NODE_MASTER_FOUND = "2" ] && [ $NODE_STANBY_FOUND = "2" ];
	then
		echo "[INFO][M: OK | S: OK] Cluster OK"
		reload_stream $NODE_MASTER_NAME $FILE_MASTER
	elif [ $NODE_MASTER_FOUND = "3" ] && [ $NODE_STANBY_FOUND = "3" ];
	then
		echo "[INFO][M: ER | S: ER] Cluster error"
	elif [ $NODE_MASTER_FOUND = "2" ] && [ $NODE_STANBY_FOUND = "3" ];
	then
		echo "[INFO][M: OK | S: ER]"
		FAILBACK_COMMANDS="
		set -x
		tar -czf $BACKUP_TODAY $PG_DATA_DIRECTORY

		sudo systemctl stop postgresql-9.6.service
		repmgr -f /var/lib/pgsql/repmgr/repmgr.conf -D /var/lib/pgsql/9.6/data -d repmgr -p 5432 -U repmgr -R postgres standby clone $NODE_MASTER_NAME --force
		sudo systemctl start postgresql-9.6.service
		repmgr -f /var/lib/pgsql/repmgr/repmgr.conf -d repmgr -p 5432 -U repmgr -R postgres standby register --force
		"
		GO_STANBY_COMMAND=$(ssh -T postgres@$NODE_FAIL_COMMAND "$FAILBACK_COMMANDS")
		reload_stream $NODE_MASTER_NAME $FILE_MASTER
		sleep 2
	elif [ $NODE_MASTER_FOUND = "3" ] && [ $NODE_STANBY_FOUND = "2" ];
	then
		echo "[INFO][M: ER | S: OK]"
		ssh -T postgres@$NODE_STANBY_NAME "repmgr -f /var/lib/pgsql/repmgr/repmgr.conf standby promote"
		sleep 2
	else
		echo "[ERROR] Not found state..."
	fi

	rm $FILE_KEY
else
	echo "File /tmp/postgres_ha_key found..."
	sleep 10
fi
