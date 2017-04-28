## Config kubectl to base64

```
echo -n "apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: 0000000000000000000000
    server: https://kubernetes
  name: gke
contexts:
- context:
    cluster: gke
    user: gke
  name: gke
current-context: gke
kind: Config
preferences: {}
users:
- name: gke
  user:
    client-certificate-data: 0000000000000000000
    password: xxxxxxxxxxxxxxxx
    username: userxxxxx" | base64 -w0
```

Value for CONF_KUBE_BASE64 in `slug-autoscaler-rc.yaml`

```
- name: CONF_KUBE_BASE64
	value: "YXBpVmVyc2lvbjogdjEKY2x1c3RlcnM6Ci0gY2x1c3RlcjoKICAgIGNlcnRpZmljYXRlLWF1dGhvcml0eS1kYXRhOiAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwCiAgICBzZXJ2ZXI6IGh0dHBzOi8va3ViZXJuZXRlcwogIG5hbWU6IGdrZQpjb250ZXh0czoKLSBjb250ZXh0OgogICAgY2x1c3RlcjogZ2tlCiAgICB1c2VyOiBna2UKICBuYW1lOiBna2UKY3VycmVudC1jb250ZXh0OiBna2UKa2luZDogQ29uZmlnCnByZWZlcmVuY2VzOiB7fQp1c2VyczoKLSBuYW1lOiBna2UKICB1c2VyOgogICAgY2xpZW50LWNlcnRpZmljYXRlLWRhdGE6IDAwMDAwMDAwMDAwMDAwMDAwMDAKICAgIHBhc3N3b3JkOiB4eHh4eHh4eHh4eHh4eHh4CiAgICB1c2VybmFtZTogdXNlcnh4eHh4"
```