# StatefulSet Autoscaler and tools

## Execution examples

```
python main.py namespace="default" url_heapster="svc-heapster/api/v1/model" autoscaler_count="5" time_query="10"
```

## Arguments

* `namespace`: Namespace of StatefulSet.
* `url_heapster`: URL to service heapster for monitoring CPU an memory.
* `autoscaler_count`: Waiting number before attempting autoscaler.
* `time_query`: Waiting time to next query of state of StatefulSet.

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