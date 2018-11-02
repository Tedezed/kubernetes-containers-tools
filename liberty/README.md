# Liberty Ingress

Image `tedezed/liberty-dynamic-ingress`

# Kube-Lego

Add to deployment of kube-lego:

```
LEGO_SUPPORTED_INGRESS_PROVIDER="nginx,liberty"
LEGO_SUPPORTED_INGRESS_CLASS="nginx,liberty"
```