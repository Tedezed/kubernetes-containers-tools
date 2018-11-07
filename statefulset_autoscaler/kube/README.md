# StatefulSet Autoscaler examples for Kubernetes

## Example Controller autoscaler

`slug-autoscaler-rc.yaml`

## Example StatefulSet

`set-example-nginx.yaml`

## Add labels to StatefulSet

```
apiVersion: apps/v1beta1
kind: StatefulSet
metadata:
  name: NAME_STATEFULSET
  labels:
    app: NAME_STATEFULSET
spec:
  serviceName: "NAME_STATEFULSET"
  replicas: 5
  template:
    metadata:
      labels:
        app: NAME_STATEFULSET
      annotations:
        pod.alpha.kubernetes.io/initialized: "true"
        slug-autoscaler/autoscaler: "true"
        slug-autoscaler/autoscaler_percent_cpu: "50"
        slug-autoscaler/autoscaler_count: "0"
        slug-autoscaler/autoreduce_normal: "true"
        slug-autoscaler/autoreduce_percent_cpu: "10"
        slug-autoscaler/min_replicas: "3"
        slug-autoscaler/max_replicas: "8"
        slug-autoscaler/sts_owner_name: "NAME_STATEFULSET"
```