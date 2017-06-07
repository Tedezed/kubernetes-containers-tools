# StatefulSet Autoscaler examples for Kubernetes

## Example Controller autoscaler

`slug-autoscaler-rc.yaml`

## Example StatefulSet

`set-example-nginx.yaml`

## Add labels to StatefulSet

```
autoscaler: "true"
autoscaler_percent_cpu: "50"
# Need autoscaler in true
autoreduce_normal: "true"
autoreduce_percent_cpu: "10"
min_replicas: "1"
max_replicas: "8"
autoscaler_count: "0"
```