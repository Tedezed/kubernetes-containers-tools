# Liberty Ingress

Image `tedezed/liberty-dynamic-ingress`

## Kube-Lego

Add to deployment of kube-lego:

```
LEGO_SUPPORTED_INGRESS_PROVIDER="nginx,liberty"
LEGO_SUPPORTED_INGRESS_CLASS="nginx,liberty"
```

## Backend modes

All backend use sticky session Nginx.

**Default**: IP backend from service.

```
-----------------       ----------------       -------
| Liberty/Nginx | ----> | Service (IP) | ----> | Pod |
-----------------       ----------------       -------
```

**Pod**: IP backend from Pod, ignore service IP.
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