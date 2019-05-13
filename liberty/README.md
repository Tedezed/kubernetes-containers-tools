# Liberty Ingress

Image `tedezed/liberty-dynamic-ingress`

## Kube-Lego

Add to deployment of kube-lego:

```
LEGO_SUPPORTED_INGRESS_PROVIDER="nginx,liberty"
LEGO_SUPPORTED_INGRESS_CLASS="nginx,liberty"
```

## Backend modes

All backend use sticky session Nginx or session affinity.

Default: IP backend from service.

```
-----------------       -----------
| Liberty/Nginx | ----> | Service |
-----------------       -----------
```

Pod: IP backend from Pod `ingress-liberty/backend-entity: pod`
```
-----------------       -------
| Liberty/Nginx | ----> | Pod |
-----------------   |   -------
                    |
                    |   -------
                    |-> | Pod |
                        -------
```