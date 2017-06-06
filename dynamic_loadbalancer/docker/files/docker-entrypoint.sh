#!/bin/bash
set -e

echo "ver 0.0.0.2"

export PYKUBE_KUBERNETES_SERVICE_HOST=kubernetes
export PYKUBE_KUBERNETES_SERVICE_PORT=$KUBERNETES_SERVICE_PORT

#echo "$KMASTER kubernetes" >> /etc/hosts
echo "$KUBERNETES_SERVICE_HOST kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts
#echo -n $CONF_KUBE_BASE64 | base64 -d > /slug_dynamic_loadbalancer/credentials/config

service rsyslog start
service haproxy start

python /slug_dynamic_loadbalancer/main.py namespace=$NAMESPACE time_query=$TIME_QUERY name_set=$NAME_SET type_balance=$TYPE_BALANCE cookie=$COOKIE type_set=$TYPE_SET
