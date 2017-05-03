#!/bin/bash
set -e

echo "ver 0.0.0.1"

echo "$KMASTER kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts
echo -n $CONF_KUBE_BASE64 | base64 -d > /slug_StatefulSet_dynamic_loadbalancer/credentials/config

python /slug_StatefulSet_dynamic_loadbalancer/main.py namespace=$NAMESPACE url_heapster=$HEAPSTER time_query=$TIME_QUERY name_set=$NAME_SET type_balance=$TYPE_BALANCE cookie=$COOKIE