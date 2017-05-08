# Dynamic load balancer for Statefulset and ReplicationController

## Execution examples

Dynamic load balancingg for only one Statefulset
```
python main.py namespace="default" url_heapster="http://heapster/api/v1/model" time_query="10" name_set="odoo" type_balance="roundrobin" cookie="true" type_set="statefulset"
```

## Arguments

* `namespace`: Namespace of StatefulSet.
* `url_heapster`: URL to service heapster for monitoring CPU an memory.
* `time_query`: Waiting time to next query of state of StatefulSet.
* `name_set`: Specify StatefulSet or "allsets" for all.
* `type_balance`: http://cbonte.github.io/haproxy-dconv/configuration-1.7.html#4.2-balance
* `cookie`
* `type_set`: For ReplicationController or StatefulSet: "rc or "statefulset".