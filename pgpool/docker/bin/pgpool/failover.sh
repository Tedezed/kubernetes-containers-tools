#!/bin/bash
# Pgpool failover Docker
# 0 - This state is only used during the initialization. PCP will never display it.
# 1 - Node is up. No connections yet.
# 2 - Node is up. Connections are pooled.
# 3 - Node is down.

#source $HOME/.bash_profile
#export PCPPASSFILE=/appl/scripts/.pcppass

function attach_node {
	echo $(date +%Y.%m.%d-%H:%M:%S.%3N)" [WARN] NODE 0 is down - try attaching node..."
    TMP=$(pcp_attach_node -h localhost -U $PG_USERNAME -n $1 -w -v)
    echo $(date +%Y.%m.%d-%H:%M:%S.%3N)" [INFO] "$TMP
}

STATUS_0=$(pcp_node_info -h localhost -U $PG_USERNAME -n 0 -w | cut -d " " -f 3)
STATUS_1=$(pcp_node_info -h localhost -U $PG_USERNAME -n 1 -w | cut -d " " -f 3)

#echo $(date +%Y.%m.%d-%H:%M:%S.%3N)" [INFO] NODE 0 status "$STATUS_0;
#echo $(date +%Y.%m.%d-%H:%M:%S.%3N)" [INFO] NODE 0 status "$STATUS_1;

if (( $STATUS_0 == 3 ))
then
    attach_node 0
fi

if (( $STATUS_1 == 3 ))
then
    attach_node 1
fi

exit 0