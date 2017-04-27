#!/bin/bash

echo "ver 0.0.0.1"

echo "$KMASTER kubernetes" >> /etc/hosts
echo "$CONF_KUBE" > /slug-containers/statefullset_autoscaler/slug_statefullset_autoscaler/credentials/config

python /slug-containers/statefullset_autoscaler/slug_statefullset_autoscaler/main.py namespace=$NAMESPACE url_heapster=$HEAPSTER autoscaler_count=$AUTOSCALER_COUNT time_query=$TIME_QUERY