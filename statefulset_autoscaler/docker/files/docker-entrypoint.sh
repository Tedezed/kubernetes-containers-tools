#!/bin/bash

echo "ver 0.0.0.3"

echo "$KMASTER kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts
echo -n $CONF_KUBE_BASE64 | base64 -d > /slug_statefulset_autoscaler/credentials/config

python /slug_statefulset_autoscaler/main.py namespace=$NAMESPACE url_heapster=$HEAPSTER autoscaler_count=$AUTOSCALER_COUNT time_query=$TIME_QUERY