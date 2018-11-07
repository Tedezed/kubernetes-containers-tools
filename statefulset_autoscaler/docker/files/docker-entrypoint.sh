#!/bin/bash

set -x

export PYKUBE_KUBERNETES_SERVICE_HOST=kubernetes
export PYKUBE_KUBERNETES_SERVICE_PORT=$KUBERNETES_SERVICE_PORT

echo "ver 2.0"
echo "$KUBERNETES_SERVICE_HOST kubernetes" >> /etc/hosts

#echo "$KMASTER kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts
#echo -n $CONF_KUBE_BASE64 | base64 -d > /slug_statefulset_autoscaler/credentials/config

python /slug_statefulset_autoscaler/main.py url_heapster=$HEAPSTER autoscaler_count=$AUTOSCALER_COUNT time_query=$TIME_QUERY