# Squirrel

Kubernetes secrets and apps passwords rotation, storage the application credentials using GPG.

<img src="https://raw.githubusercontent.com/tedezed/kubernetes-containers-tools/master/docs/img/Squirrel.png">

# Install Squirrel

```
kubectl create -f https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/squirrel/install.yaml
```

## Create custom modules for your application

- [Example module](https://github.com/Tedezed/kubernetes-containers-tools/tree/master/squirrel/docker/squirrel/nuts_manager/modules/origin-example-module)


## Create Nutcrackers

Example Admin:
```
kubectl delete nutcrackers admin
kubectl delete clusterrolebinding admin-squirrel
cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: admin
type: Opaque
data:
  email: "admin@example.com"
  keypub: $(cat $HOME/.squirrel/local.pub | base64 -w0)
permissions:
  - "*/*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-squirrel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: squirrel-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: admin@example.com
EOF
```

Example User:
```
kubectl delete nutcrackers user
cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: admin
type: Opaque
data:
  email: "user@example.com"
  keypub: $(cat $HOME/.squirrel/local.pub | base64 -w0)
permissions:
  # - "namespace/service"
  - "demo1/app-demo1"
  - "demo2/app-demo2"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: user-view-squirrel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: squirrel-view-nuts
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: user@example.com
EOF
```

Run Job if you need rotation now:
```
kubectl delete job -n kube-system squirrel-rotation-now
kubectl create job --from=cronjob/squirrel -n kube-system squirrel-rotation-now
```

Rotation now only for apps:
```
kubectl delete job -n kube-system squirrel-rotation-now
kubectl create -f https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/squirrel/kubernetes/squirrel-job-rotation-apps.yaml
```

Rotation now only for secrets:
```
kubectl delete job -n kube-system squirrel-rotation-now
kubectl create -f https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/squirrel/kubernetes/squirrel-job-rotation-secrets.yaml
```
