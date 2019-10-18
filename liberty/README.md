# Liberty Ingress

Alternative Kubernetes ingress with easy customization with Python and jinja templates

Image `tedezed/liberty-dynamic-ingress`

## Backend modes

All backend use sticky session Nginx.

**Service**: IP backend from service.
Annotation `ingress-liberty/backend-entity: service`
```
-----------------       ----------------       -------
| Liberty/Nginx | ----> | Service (IP) | ----> | Pod |
-----------------       ----------------       -------
```

**Pod** (default): IP backend from Pod, ignore service IP.
Annotation `ingress-liberty/backend-entity: pod` for session affinity.
```
-----------------       ------------
| Liberty/Nginx | ----> | Pod (IP) |
-----------------   |   ------------
                    |
                    |   ------------
                    |-> | Pod (IP) |
                        ------------
```


## Start/Stop namespace like Heroku using ingress

- Add the next annotations to ingress: `ingress-liberty/start-stop: "true"`
- You can exclude a deploy or an rc so that it is not affected in the namespace, using the annotation: `ingress-liberty/start-stop: "false"`

#### Deploy Ingress Liberty and filebeat

Operation Diagram
<img src="https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/tools/images/liberty_start-stop.png">


Env variables Liberty:
- ELK="false"

```
  -----------------
  |  Pod Liberty  |
  |               |
  | ------------- |
  | | Container | |
  | |  Liberty  | |
  | ------------- |
  | ------------- |
  | | Container | |                                     -------------------
  | | Filebeat  | --> POST Ingest logs ---------------> |   ELK Stack     |
  | ------------- |    /var/log/nginx/access.log        | - Logstash      |
  -----------------    /var/log/nginx/custom_error.log  | - ElasticSearch |
                                                        -------------------
```

#### Deploy ELK Liberty mode start

Env variables:
- ELK="true"
- ELK_MODE="start"
- TIME_QUERY="35"
- ELK_HOST="elasticsearch-client.namespace.svc.cluster.local"
- ELK_LIBERTY_NAMES="liberty-test-1 liberty-test-2"

Functioning:
- If the ingress was visited but returned an error 502 (usually because it is stopped) it tries to start
```
  -----------------
  |  Pod Liberty  |
  |               |
  | ------------- |
  | | Container | <---- GET today logs <--- [ ELK Stack ]
  | |  Liberty  | |      query : {"ingress" : "host_domain_X"}
  | ------------- |              {"source": "/var/log/nginx/custom_error.log"}
  |---------------|
```

#### Cronjob [ 00 00 * * * ] ELK Liberty mode stop

Env variables:
- ELK="true"
- ELK_MODE="stop"
- ELK_HOST="elasticsearch-client.namespace.svc.cluster.local"
- ELK_LIBERTY_NAMES="liberty-test-1 liberty-test-2"

Functioning:
- If the ingress was not visited yesterday it stops
```
  -----------------
  |  Pod Liberty  |     - Started once a day
  |               |
  | ------------- |
  | | Container | <---- GET yesterday logs <--- [ ELK Stack ]
  | |  Liberty  | |      query : {"ingress" : "host_domain_X"}
  | ------------- |              {"source": "/var/log/nginx/access.log"}
  |---------------|
```


## Kube-Lego

Add to deployment of kube-lego:

```
LEGO_SUPPORTED_INGRESS_PROVIDER="nginx,liberty"
LEGO_SUPPORTED_INGRESS_CLASS="nginx,liberty"
```