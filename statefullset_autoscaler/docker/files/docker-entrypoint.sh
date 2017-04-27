#!/bin/bash

echo "ver 0.0.0.1"

echo "$KMASTER kubernetes" >> /etc/hosts
echo "$CONF_KUBE" > /slug-containers/credentials/config

python /slug-containers/main.py namespace=$NAMESPACE url_heapster=$HEAPSTER autoscaler_count=$AUTOSCALER_COUNT time_query=$TIME_QUERY